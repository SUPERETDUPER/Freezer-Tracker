"""
MIT License

Copyright (c) 2017 Martin Staadecker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Frames dealing with adding items to the database.

Tracks the current selection through productInfo which gets reset when coming back to the frame.
"""
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
