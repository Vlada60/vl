import valueLine
import fitz

docNames: list[str] = []

docNames.append("./tests/VL KO 2301.pdf")
docNames.append("./tests/VL META 2302.pdf")
docNames.append("./tests/VL ANF 2301.pdf")
docNames.append("./tests/VL HBI 2504.pdf")
docNames.append("./tests/VL JBL 2503.pdf")
docNames.append("./tests/VL KO 2504.pdf")
docNames.append("./tests/VL LKQ 2506.pdf")
docNames.append("./tests/VL MCD 2505.pdf")
docNames.append("./tests/VL MRVL 2503.pdf")
docNames.append("./tests/VL NKE 2504.pdf")
docNames.append("./tests/VL SIGI 2505.pdf")
docNames.append("./tests/VL SMCI 2506.pdf")
docNames.append("./tests/VL TECH 2505.pdf")
docNames.append("./tests/VL TRU 2505.pdf")
docNames.append("./tests/VL TSCO 2503.pdf")
docNames.append("./tests/VL VZ 2506.pdf")
blankdocname = "./tests/blank.pdf"

for docName in docNames:
    print("")
    print(docName.split('/')[2])
    doc = fitz.open(docName)
    page = doc[0]
    (quallity, price) = valueLine.get_data(page)
    doc.save(docName.rstrip(".pdf") + "-tmp.pdf")

blankdoc = fitz.open(blankdocname)
page = blankdoc[0]
(quallity, price) = valueLine.get_data(page)
