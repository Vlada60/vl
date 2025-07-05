"""
Script showing how to select only text that is contained in a given rectangle
on a page.

We use "page.get_textbox", which is available since PyMuPDF v1.18.0.
The decision on what whill be included is made by character, so while much
simpler to use than the other script in this folder, it will ignore word
integrity and cut through any overlaps.

There also is no logic that maintains natural reading order, so text will
appear as stored in the document.

"""
import fitz

def get_text(page: fitz.Page):
    print("timeliness " + page.get_textbox(timelinessRect))
    print("safety " + page.get_textbox(safetyRect))
    print("beta " + page.get_textbox(betaRect))
    print("rating " + page.get_textbox(ratingRect))
    # print(page.get_textbox(rightRect))
    right = page.get_textbox(rightRect).splitlines()
    i = 0
    salesHeight = 305
    for line in right:
        if line.__contains__("Revenues (") or line.__contains__("Sales ("):
            salesHeight = 215 + i*9
        i = i+1
    projectedSalesRect = fitz.Rect(550,salesHeight,569,salesHeight + 7)
    print("projected sales " + page.get_textbox(projectedSalesRect))
    

doc1 = fitz.open("/Users/nina/Downloads/download/VL KO 2301.pdf")  # any supported document type
doc2 = fitz.open("/Users/nina/Downloads/download/VL META 2302.pdf")  
doc3 = fitz.open("/Users/nina/Downloads/download/VL ANF 2301.pdf")  

page1 = doc1[0]
page2 = doc2[0]
page3 = doc3[0]

"""
-------------------------------------------------------------------------------
Identify the rectangle.
-------------------------------------------------------------------------------
"""
timelinessRect = fitz.Rect(88,58,90,60) # this annot has been prepared for us!
safetyRect = fitz.Rect(88,68,90,74) 
betaRect = fitz.Rect(62,91.5,75,97.5) 
ratingRect = fitz.Rect(550,725.5,563,731)
rightRect = fitz.Rect(478,215,540,404)

# Now we have the rectangle ---------------------------------------------------

print("")
print("Coca cola:")
get_text(page1)
print("")
print("Meta:")
get_text(page2)
print("")
print("A:")
get_text(page3)
