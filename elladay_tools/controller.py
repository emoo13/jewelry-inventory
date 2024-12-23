from PIL import Image, ImageDraw, ImageFont
import model
import textwrap
import os

class MongoController:
    def __init__(self):
        self.model_obj = model.MongoModel()

    def process_products(self, query_data):
        table_list = []
        for product in query_data:
            if not product["image_urls"]:
                product["image_urls"] = [""]

            product_dict = {
                    "image": product["image_urls"][0],
                    "jewelry_name": product["product_name"],
                    "quantity": product["quantity_in_stock"],
                    "manufacturer": product["brand"],
                    "sku": product["sku"],
                    "platform": product["store_platform"],
                    "created_date": product["date_added"],
                    "sell_price": product["unit_price"],
                    "sold_status": product["sell_status"],
                    "shop_status": product["status"],
                    "item_id": product["_id"],
                }
            table_list.append(product_dict)
        return table_list
    
    def process_materials(self, query_data):
        materials_list = [sub['name'] for sub in query_data]
        materials_names = [word.capitalize() for word in materials_list]
        materials_names.insert(0, "")
        return materials_names
    
    def process_subgemstones(self, query_data, selected_gem):
        gem_dict = [item for item in query_data if item.get('name') == selected_gem.lower()]
        sub_gem_list = [sub['types'] for sub in gem_dict][0]
        value_list = [word.capitalize() for word in sub_gem_list]
        return value_list

    def process_status_table(self, status_dict):
        key_list = ["photo"]
        for key, value in status_dict.items():
            if value is True:
                key_list.append(key)
            elif value is False:
                return key_list[-1]
            else:
                return "Boxing"
            
    def process_dimensions(self, height, dim_data, pt_obj_list):
        len_wid_list = ["length", "width"]
        if height:
            len_wid_list.append("height")
        
        for i, obj in enumerate(pt_obj_list):
            try:
                if not dim_data[len_wid_list[i]]:
                    obj.setPlainText("")
                else:
                    obj.setPlainText(str(dim_data[len_wid_list[i]]))
            except KeyError:
                print("No key {} in dimension data: {}".format(i, dim_data))
    
    def lowercase_nested_dict(self, val):
        if isinstance(val, dict):  # If val is a dictionary
            return {key: self.lowercase_nested_dict(value) for key, value in val.items()}
        elif isinstance(val, str):  # If val is a string
            return val.lower() if val is not None else val
        else:
            return val  # If it's neither a dictionary nor a string, return as is

    def process_search(self, text, query_data):
        table_data = []
        for val in query_data:
            lowercase_values = self.lowercase_nested_dict(val)
            if text.lower() in lowercase_values.values():
                table_data.append(val)
        return table_data

    def handle_imgs(self, sku, product_name, img_list):
        if sku:
            results = self.model_obj.sku_query(sku)
            query_val = sku
            query_key = "product.sku"
            # Check the image isn't already in the database
        elif product_name:
            results = self.model_obj.product_name_query(product_name)
            query_val = product_name
            query_key = "product.product_name"
        else:
            return None

        if results:
            orig_image_list = results["image_urls"]
        else:
            orig_image_list = []
        new_list = [item for item in img_list if item not in orig_image_list]
        final_list = orig_image_list + new_list
        return final_list, query_val, query_key

    # Function to create a 2x3 label grid as a PNG image
    def create_label_grid(self,
                          name,
                          price,
                          brand,
                          sku,
                          checkboxes,
                          created,
                          label_loc):
        if not label_loc:
            label_loc = os.path.expanduser("~")
        # Label width
        label_width = 400
        checkbox_size = 15
        spacing = 10
        string_checkboxes = [
                "Photo",
                "Measuring",
                "Cleaning",
                "Repairing",
                "Weighing",
                "Listing",
                "Boxing"
            ]
        # Create a blank white image (initial height is 1, will be updated dynamically)
        img = Image.new("RGB", (label_width, 1), "white")
        draw = ImageDraw.Draw(img)

        # Load regular and bold fonts
        regular_font = ImageFont.truetype("arial.ttf", size=14)  # Adjust the path to your font
        bold_font = ImageFont.truetype("arialbd.ttf", size=14)   # Adjust the path to your bold font

        # Helper function to wrap text
        def wrap_text(text, font, max_width):
            wrapped_lines = []
            for line in text.splitlines():  # Handle multi-line strings
                width, _ = draw.textbbox((0, 0), line, font=font)[2:4]
                if width > max_width:
                    wrapped_lines.extend(textwrap.wrap(line, width=int(max_width / 7)))  # Approx. 7px per char
                else:
                    wrapped_lines.append(line)
            return wrapped_lines

        # Helper function to calculate text height
        def get_text_height(text, font):
            bbox = draw.textbbox((0, 0), text, font=font)
            return bbox[3] - bbox[1]

        # Helper function to draw wrapped text and calculate total height
        def draw_wrapped_text(draw, text, font, x, y, max_width, spacing):
            lines = wrap_text(text, font, max_width)
            for line in lines:
                draw.text((x, y), line, font=font, fill="black")
                y += get_text_height(line, font) + spacing
            return y, len(lines)  # Return the final y position and the number of lines drawn

        # Max width for wrapping text
        max_text_width = label_width - 120  # Leave space for labels

        # Start drawing at position
        x = 10
        y = 10
        label_height = 0  # Keep track of the height required
        price = "$" + price
        # Draw bold labels and wrapped text, updating the height dynamically
        y, _ = draw_wrapped_text(draw, "Name:", bold_font, x, y, max_text_width, spacing)
        y, _ = draw_wrapped_text(draw, name, regular_font, x + 100, y, max_text_width, spacing)

        y, _ = draw_wrapped_text(draw, "Price:", bold_font, x, y, max_text_width, spacing)
        y, _ = draw_wrapped_text(draw, price, regular_font, x + 100, y, max_text_width, spacing)

        y, _ = draw_wrapped_text(draw, "Brand:", bold_font, x, y, max_text_width, spacing)
        y, _ = draw_wrapped_text(draw, brand, regular_font, x + 100, y, max_text_width, spacing)

        y, _ = draw_wrapped_text(draw, "SKU:", bold_font, x, y, max_text_width, spacing)
        y, _ = draw_wrapped_text(draw, sku, regular_font, x + 100, y, max_text_width, spacing)

        y, _ = draw_wrapped_text(draw, "Created:", bold_font, x, y, max_text_width, spacing)
        y, _ = draw_wrapped_text(draw, created, regular_font, x + 100, y, max_text_width, spacing)

        # Additional space before checkboxes
        y += spacing * 2

        # Calculate the height required for checkboxes
        for checkbox in checkboxes:
            y += checkbox_size + spacing

        # Update the image height based on the total required height
        label_height = y
        img = img.resize((label_width, label_height), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(img)

        # Draw the content again with updated height
        y = 10
        draw.text((x, y), "Name:", font=bold_font, fill="black")
        y = draw_wrapped_text(draw, name, regular_font, x + 100, y, max_text_width, spacing)[0]

        draw.text((x, y), "Price:", font=bold_font, fill="black")
        y = draw_wrapped_text(draw, price, regular_font, x + 100, y, max_text_width, spacing)[0]

        draw.text((x, y), "Brand:", font=bold_font, fill="black")
        y = draw_wrapped_text(draw, brand, regular_font, x + 100, y, max_text_width, spacing)[0]

        draw.text((x, y), "SKU:", font=bold_font, fill="black")
        y = draw_wrapped_text(draw, sku, regular_font, x + 100, y, max_text_width, spacing)[0]

        draw.text((x, y), "Created:", font=bold_font, fill="black")
        y = draw_wrapped_text(draw, created, regular_font, x + 100, y, max_text_width, spacing)[0]

        for i, checkbox in enumerate(string_checkboxes):
            # Draw the checkbox
            draw.rectangle(
                [x, y, x + checkbox_size, y + checkbox_size],
                outline="black",
                width=1
            )
            if checkboxes[i]:
                # Draw an "X" or filled rectangle for the check
                draw.line(
                    [(x, y), (x + checkbox_size, y + checkbox_size)],
                    fill="black",
                    width=2
                )
                draw.line(
                    [(x, y + checkbox_size), (x + checkbox_size, y)],
                    fill="black",
                    width=2
                )

            # Draw the label
            draw.text((x + checkbox_size + spacing, y), checkbox, font=regular_font, fill="black")
            y += checkbox_size + spacing
        # Save or display the image
        img.show()
        image_name = "Label_" + sku + ".png"
        label_name = os.path.join(label_loc, image_name)
        img.save(label_name)

        return label_name

# # Create a blank white image
        # img = Image.new("RGB", (label_width, label_height), "white")
        # draw = ImageDraw.Draw(img)

        # # Load a font (adjust the path to an installed font file if needed)
        # font = ImageFont.load_default()

        # # Calculate text height using `ImageDraw.textsize`
        # text_height = self.get_text_height("Sample Text", font, draw)

        # # Text positions
        # x = 10
        # y = 10

        # # Draw text lines
        # draw.text((x, y), f"Name: {name}", font=font, fill="black")
        # y += text_height + spacing
        # draw.text((x, y), f"Price: {price}", font=font, fill="black")
        # y += text_height + spacing
        # draw.text((x, y), f"Brand: {brand}", font=font, fill="black")
        # y += text_height + spacing
        # draw.text((x, y), f"SKU: {sku}", font=font, fill="black")
        # y += text_height + spacing
        # draw.text((x, y), f"Created: {created}", font=font, fill="black")
        # y += text_height + spacing * 2

        # # Draw checkboxes with labels
        # for checkbox in checkboxes:
        #     # Draw checkbox
        #     draw.rectangle(
        #         [x, y, x + checkbox_size, y + checkbox_size],
        #         outline="black",
        #         width=1
        #     )
        #     # Draw checkbox label
        #     draw.text((x + checkbox_size + spacing, y), checkbox, font=font, fill="black")
        #     y += checkbox_size + spacing
        # Label dimensions