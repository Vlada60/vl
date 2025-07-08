import extract
import fitz

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
