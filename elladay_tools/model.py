import pymongo
from bson.objectid import ObjectId
import pandas as pd
import os

PRODUCT_ID_MONGO = '67686573e3da599d42c6db51'
GEMSTONE_ID_MONGO = '676853d7e3da599d42c6db50'
METADATA_ID_MONGO = '6767ba05bcb627079b8d3806'
class MongoModel:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://elladaysoptera:Bringmeyou13@elladaysoptera.4q5ij.mongodb.net/")
        self.db = self.client["inventory"]

    def connection_to_mongo(self):
        try:
            try:
                self.client.admin.command('ping')
                print("Connected to MongoDB!")
            except Exception as e:
                print("Failed to connect to MongoDB:", e)
            return self.db["products"]
        except Exception as e:
            print("Error connecting to MongoDB:", e)
        return None
    
    def shade_query(self, selected_text):
        color_text = "colors." + selected_text
        query = { color_text: { "$exists": True } }
        projection = { "_id": 0, color_text + ".shades": 1 }
        result = self.db["products"].find(query, projection)
        return result
    
    def sku_query(self, item_id):
        for result in self.db["products"].find({"product.sku": item_id}):
            for arr in result["product"]:
                if arr["sku"] == item_id:
                    return arr

    def product_name_query(self, name):
        for result in self.db["products"].find({"product.product_name": name}):
            for arr in result["product"]:
                if arr["product_name"] == name:
                    return arr

    def color_query(self):
        query = { "colors": { "$exists": True } }
        projection = { "_id": 0, "colors": 1 }
        colors_query = self.db["products"].find(query, projection)

        for x in colors_query:
            colors=list(x["colors"].keys())
        color_list = [word.capitalize() for word in colors]
        color_list.insert(0, "")
        return color_list
    
    def condition_query(self):
        cond_list = self.general_query("conditions")
        return cond_list
    
    def category_query(self):
        cat_list = self.general_query("categories")
        return cat_list

    def platforms_query(self):
        plat_list = self.general_query("platforms")
        return plat_list

    def sell_status_query(self):
        sell_list = self.general_query("sell-stats")
        return sell_list

    def subcategory_query(self):
        subcat_list = self.general_query("sub-categories")
        return subcat_list

    def product_query(self):
        prod_list = self.db["products"].distinct("product")
        return prod_list
    
    def gem_query(self):
        gem_list = self.db["products"].distinct("gemstones")
        return gem_list
    
    def metal_query(self):
        metal_list = self.db["products"].distinct("metals")
        return metal_list
    
    def clarity_query(self):
        clarity_list = self.db["products"].distinct("gemstone_clarity_types")
        acronym_list = [sub['acronym'] for sub in clarity_list]
        value_list = [word.capitalize() for word in acronym_list]
        value_list.insert(0, "")
        return value_list
    
    def plating_query(self):
        plating_list = self.db["products"].distinct("plating_types")
        plating_names = [sub['name'] for sub in plating_list]
        value_list = [word.capitalize() for word in plating_names]
        value_list.insert(0, "")
        return value_list

    def cut_query(self):
        cut_list = self.db["products"].distinct("gemstone_cuts")
        cut_data = [sub['name'] for sub in cut_list]
        value_list = [word.capitalize() for word in cut_data]
        value_list.insert(0, "")
        return value_list
    
    def general_query(self, key):
        query = self.db["products"].distinct(key)
        value_list = [word.capitalize() for word in query]
        value_list.insert(0, "")
        return value_list

    def delete_from_db(self, prod_id):
        filter = {
            "product._id": prod_id
        }

        # Define the update operation to remove that product from the 'product' array
        update = {
            "$pull": {
                "product": {
                    "_id": prod_id
                }
            }
        }

        # Perform the update operation
        result = self.db["products"].update_one(filter, update)

    def delete_gemstones_from_db(self, key, value, types=False, parent_key=None):
        if types:
            result = self.db["products"].update_many(
                {"gemstones.types": {"$exists": True}},
                {"$pull": {"gemstones.$[].types": value}}
            )
        else:
            wow = parent_key + "." + key
            result = self.db["products"].update_one(
                {wow : value},
                {"$pull": {parent_key: {key: value}}}
            )
        if result.modified_count > 0:
            print("Document updated successfully.")
        elif result.matched_count > 0:
            print("Document matched, but no updates were made.")
        else:
            print("No matching document found.")

    def update_imgs(self, query_key, query_val, final_list):
        result = None
        result = self.db["products"].update_one(
            {query_key: query_val},
            {"$set": {"product.$.image_urls": final_list}}
        )

        if result:
                if result.modified_count > 0:
                    print("Product updated successfully.")
                else:
                    print("No changes were made to the product.")

    def update_generic_data(self, filter_text, val, dictionary):
        result = self.db["products"].update_one(
                        {filter_text: val},
                        {"$set": dictionary}
                    )

    def create_new_entry(self, data_dict, key, document_id):
        woop = data_dict[key][0]
        # Merge the new entry with the original dictionary
        # result = self.db["products"].update_one(
        #     {},  # Add a filter here if you want to target a specific document, or use {} to insert into the first document
        #     {"$push": {key: data_dict[key][0]}},  # Push the new gemstone into the 'gemstones' array
        #     upsert=True  # If no document exists, it will insert one
        # )
        result = self.db["products"].update_one(
            {"_id": ObjectId(document_id)},  # Filter to target the specific document you want to update
            {"$push": {"gemstones": data_dict}}  # Push the new gemstone into the 'gemstones' array
        )

    def export_to_excel(self, excel_location):
        product_id = PRODUCT_ID_MONGO  # Replace with the specific _id of the product you're looking for
        document = self.db["products"].find_one({"_id": ObjectId(product_id)})
        value = document["product"]
        df = pd.DataFrame(value)
        # Check if the document was found
        if document:
            if excel_location:
                output_file = os.path.join(excel_location, "product.xlsx")
            else:
                home = os.path.expanduser("~")
                output_file = os.path.join(home, "product.xlsx")

            df.to_excel(output_file, index=False, engine='openpyxl')

            print(f"Data exported to {output_file}")
        else:
            print("Product not found.")

    def update_data(self, sku, product_name, update_data):
            data_dict = self.generate_db_dict(update_data)
            document_id = PRODUCT_ID_MONGO
            result = None

            if sku:
                query_result = self.sku_query(sku)
                if query_result:
                    result = self.db["products"].update_one(
                        {"product.sku": sku},  # Filter the document by sku
                        {"$set": data_dict}
                    )
                else:
                    data_dict = self.generate_new_db_dict(update_data)
                    new_entry = {"_id": str(ObjectId())}

                    # Merge the new entry with the original dictionary
                    updated_dict = {**new_entry, **data_dict}
                    result = self.db["products"].update_one(
                            {"_id": ObjectId(document_id)},  # Filter by `_id`
                            {"$push": {"product": updated_dict}}  # Use `$push` to add to the array
                        )
                    # new_result = self.db["products"].insert_one(data_dict)
            elif product_name:
                query_result = self.product_name_query(product_name)
                if query_result:
                    result = self.db["products"].update_one(
                        {"product.product_name": product_name},  # Filter the document by product_name
                        {"$set": {
                            "product.$": update_data  # Update the entire product array element with the new data
                        }}
                    )
                else:
                    data_dict = self.generate_new_db_dict(update_data)
                    new_entry = {"_id": str(ObjectId())}

                    # Merge the new entry with the original dictionary
                    updated_dict = {**new_entry, **data_dict}
                    result = self.db["products"].update_one(
                            {"_id": ObjectId(document_id)},  # Filter by `_id`
                            {"$push": {"product": updated_dict}}  # Use `$push` to add to the array
                        )

            else:
                print("Couldn't create or update the product database")

            if result:
                if result.modified_count > 0:
                    print("Product updated successfully.")
                else:
                    print("No changes were made to the product.")

    def generate_db_dict(self, update_data):
        return {
                "product.$.product_name": update_data["product_name"],
                "product.$.category": update_data["category"],
                "product.$.subcategory": update_data["subcategory"],
                "product.$.color": update_data["color"],
                "product.$.shade": update_data["shade"],
                "product.$.condition": update_data["condition"],
                "product.$.handmade": update_data["handmade"],
                "product.$.store_platform": update_data["store_platform"],
                "product.$.sku": update_data["sku"],
                "product.$.quantity_in_stock": update_data["quantity_in_stock"],
                "product.$.unit_price": update_data["unit_price"],
                "product.$.researched_price": update_data["researched_price"],
                "product.$.sell_status": update_data["sell_status"],
                "product.$.label_printed": update_data["label_printed"],
                "product.$.gemstone": update_data["gemstone"],
                "product.$.gemstone_details.cut": update_data["gemstone_details"]["cut"],
                "product.$.gemstone_details.clarity": update_data["gemstone_details"]["clarity"],
                "product.$.gemstone_details.carat_weight": update_data["gemstone_details"]["carat_weight"],
                "product.$.gemstone_details.type": update_data["gemstone_details"]["type"],
                "product.$.metal_type": update_data["metal_type"],
                "product.$.metal_details.carats": update_data["metal_details"]["carats"],
                "product.$.metal_details.plated": update_data["metal_details"]["plated"],
                "product.$.dimensions.chain.length": update_data["dimensions"]["chain"]["length"],
                "product.$.dimensions.chain.height": update_data["dimensions"]["chain"]["height"],
                "product.$.dimensions.chain.width": update_data["dimensions"]["chain"]["width"],
                "product.$.dimensions.clasp.length": update_data["dimensions"]["clasp"]["length"],
                "product.$.dimensions.clasp.height": update_data["dimensions"]["clasp"]["height"],
                "product.$.dimensions.focal.width": update_data["dimensions"]["clasp"]["width"],
                "product.$.dimensions.focal.length": update_data["dimensions"]["focal"]["length"],
                "product.$.dimensions.focal.height": update_data["dimensions"]["focal"]["height"],
                "product.$.dimensions.pin.length": update_data["dimensions"]["pin"]["length"],
                "product.$.dimensions.pin.lenwidthgth": update_data["dimensions"]["pin"]["width"],
                "product.$.weight_before": update_data["weight_before"],
                "product.$.weight_after": update_data["weight_after"],
                "product.$.brand": update_data["brand"],
                "product.$.date_added": update_data["date_added"],
                "product.$.last_modified": update_data["last_modified"],
                "product.$.date_posted": update_data["date_posted"],
                "product.$.tags": update_data["tags"],
                "product.$.image_urls": update_data["image_urls"],
                "product.$.status.photo": update_data["status"]["photo"],
                "product.$.status.measuring": update_data["status"]["measuring"],
                "product.$.status.cleaning": update_data["status"]["cleaning"],
                "product.$.status.repairing": update_data["status"]["repairing"],
                "product.$.status.weighing": update_data["status"]["weighing"],
                "product.$.status.listing": update_data["status"]["listing"],
                "product.$.status.boxing": update_data["status"]["boxing"],
                "product.$.listing_url": update_data["listing_url"],
                "product.$.notes": update_data["notes"],
                "product.$.label_location": update_data["label_location"]
            }
    def generate_new_db_dict(self, update_data):
        return {
                "product_name": update_data["product_name"],
                "category": update_data["category"],
                "subcategory": update_data["subcategory"],
                "color": update_data["color"],
                "shade": update_data["shade"],
                "condition": update_data["condition"],
                "handmade": update_data["handmade"],
                "store_platform": update_data["store_platform"],
                "sku": update_data["sku"],
                "quantity_in_stock": update_data["quantity_in_stock"],
                "unit_price": update_data["unit_price"],
                "researched_price": update_data["researched_price"],
                "sell_status": update_data["sell_status"],
                "label_printed": update_data["label_printed"],
                "gemstone": update_data["gemstone"],
                "gemstone_details" : {
                    "cut": update_data["gemstone_details"]["cut"],
                    "clarity": update_data["gemstone_details"]["clarity"],
                    "carat_weight": update_data["gemstone_details"]["carat_weight"],
                    "type": update_data["gemstone_details"]["type"]
                },
                "metal_type": update_data["metal_type"],
                "metal_details" : {
                    "carats": update_data["metal_details"]["carats"],
                    "plated": update_data["metal_details"]["plated"]
                },
                "dimensions" : {
                    "chain" : {
                        "length": update_data["dimensions"]["chain"]["length"],
                        "height": update_data["dimensions"]["chain"]["height"],
                        "width": update_data["dimensions"]["chain"]["width"]
                    },
                    "clasp" : {
                        "length": update_data["dimensions"]["clasp"]["length"],
                        "height": update_data["dimensions"]["clasp"]["height"],
                        "width": update_data["dimensions"]["clasp"]["width"]
                    },
                    "focal" : {
                        "length": update_data["dimensions"]["focal"]["length"],
                        "height": update_data["dimensions"]["focal"]["height"],
                        "width": update_data["dimensions"]["focal"]["width"]
                    },
                    "pin" : {
                        "length": update_data["dimensions"]["pin"]["length"],
                        "height": update_data["dimensions"]["pin"]["width"]
                    }
                },
                "weight_before": update_data["weight_before"],
                "weight_after": update_data["weight_after"],
                "brand": update_data["brand"],
                "date_added": update_data["date_added"],
                "last_modified": update_data["last_modified"],
                "date_posted": update_data["date_posted"],
                "tags": update_data["tags"],
                "image_urls": update_data["image_urls"],
                "status" : {
                    "photo": update_data["status"]["photo"],
                    "measuring": update_data["status"]["measuring"],
                    "cleaning": update_data["status"]["cleaning"],
                    "repairing": update_data["status"]["repairing"],
                    "weighing": update_data["status"]["weighing"],
                    "listing": update_data["status"]["listing"],
                    "boxing": update_data["status"]["boxing"]
                },
                "listing_url": update_data["listing_url"],
                "notes": update_data["notes"],
                "label_location": update_data["label_location"]
            }