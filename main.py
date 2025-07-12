import valueLine
import vlTypes
import fitz
import api

docname = "./tests/VL META 2302.pdf"

doc = fitz.open(docname)

page = doc[0]

(quality, price) = valueLine.get_data(page)

api.insert_to_sheets(quality, price)

doc.save(docname.rstrip(".pdf") + "-tmp.pdf")
