from gspread.utils import ValueInputOption
import extract
import fitz
import gspread

gc = gspread.oauth(credentials_filename="./credentials.json")
try:
    sheet = gc.open("the sheet")
except gspread.exceptions.SpreadsheetNotFound:
    sheet = gc.copy("1lBct8NGRyz0lV3qLV-MuE3olsJl_871OibU6ExkoMrE", "the sheet")

qualityWorksheet = sheet.worksheet("Quality")
priceWorksheet = sheet.worksheet("Price")

qualityWorksheet.batch_update([
    {
        'range': 'E18',
        'values': [['2']]
    }
], value_input_option=ValueInputOption.user_entered)

text = "9"
number = "21"
priceWorksheet.batch_update([
    {
        'range': 'Q33:R33',
        'values': [[text]]
    },
    {
        'range': 'Q35:R35',
        'values': [[number]]
    }
], value_input_option=ValueInputOption.user_entered)

doc1name = "/home/vlada/Desktop/VL KO 2301.pdf"
doc2name = "/home/vlada/Desktop/VL META 2302.pdf"
doc3name = "/home/vlada/Desktop/VL ANF 2301.pdf"
doc1name = "/home/vlada/Desktop/blank.pdf"

doc1 = fitz.open(doc1name)  # any supported document type
doc2 = fitz.open(doc2name)
doc3 = fitz.open(doc3name)

page1 = doc1[0]
page2 = doc2[0]
page3 = doc3[0]


# Now we have the rectangle ---------------------------------------------------
# print("")
# print("Coca cola:")
# extract.get_text(page1)
# print("")
# print("Meta:")
# extract.get_text(page2)
# print("")
# print("ABERCROMBIE:")
# extract.get_text(page3)
#
doc1.save(doc1name.rstrip(".pdf") + "-tmp.pdf")
doc2.save(doc2name.rstrip(".pdf") + "-tmp.pdf")
doc3.save(doc3name.rstrip(".pdf") + "-tmp.pdf")
