# This path determines where the database will be uploaded and copied
upload_path = "/mnt/FILE03/database_read_only"

# Local database path
local_path = "./database"

# List of meats and sub-types of meats.
# Format :
# [("Meat type 1", ["Sub-type 1", "Sub-type 2"]),
# ("Meat type 2", ["Sub-type 1", "Sub-type 2"])]

meat_types = [("Turkey", ["Breast", "Thigh", "Skin", "Fine textured", "Scap", "MSM", "Dark trim", "White trim", "Fat"]),
              ("Chicken",
               ["Breast", "Thigh", "Skin", "Fine textured", "MSM", "Wings", "Drums", "Dark trim", "White trim"]),
              ("Pork",
               ["Backfat", "Ham fat", "Belly", "Whole Ham", "Picnic shoulder", "Shanks", "Skin", "Loin", "Tenderloin",
                "Hearts", "Jowls", "Fine textured"]),
              ("Beef",
               ["50/50 trim", "60/40 trim", "65/35 trim", "70/30 trim", "80/20 trim", "85/15 trim", "90/10 trim",
                "Chuck", "Eye of round", "Inside", "Outside", "Heart"])]
