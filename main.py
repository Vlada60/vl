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

def search_for(text, rectangle: fitz.Rect, page: fitz.Page) -> fitz.Rect:
    foundRectangle = page.search_for(text, clip=rectangle)
    if(foundRectangle.__len__() > 0):
        return foundRectangle[0]
    else:
        return fitz.Rect(0,0,0,0)

def text_millions_in_number(number: str) -> float:
    tmp = number.split()
    if tmp[1].__contains__("bill"):
        return float(tmp[0].replace(",",""))
    elif tmp[1].__contains__("mill"):
        return float(tmp[0].replace(",",""))/1000
    return 0

def get_left_text(page: fitz.Page, rectangle: fitz.Rect):
    debtRectangle = search_for("Total Debt", rectangle, page)
    debt = page.get_textbox(fitz.Rect(debtRectangle.x1,debtRectangle.y0,debtRectangle.x1+35,debtRectangle.y1)).splitlines()
    debt = debt[0].split("$")[1]
    print("")
    print(debt)
    print(text_millions_in_number(debt))

    marketCapRectangle = search_for("MARKET CAP", rectangle, page)
    marketCap = page.get_textbox(fitz.Rect(marketCapRectangle.x1+3,marketCapRectangle.y0,marketCapRectangle.x1+35,marketCapRectangle.y1)).splitlines()
    marketCap = marketCap[0].split("$")[1]
    print("")
    print(marketCap)
    print(text_millions_in_number(marketCap))

    salesRectangle = search_for("Sales", rectangle, page)
    if salesRectangle != fitz.Rect(0,0,0,0):
        sales = page.get_textbox(fitz.Rect(salesRectangle.x0+82,salesRectangle.y0+3,salesRectangle.x0+135,salesRectangle.y1-3)).splitlines()
        print("")
        print(sales)
    else:
        salesRectangle = search_for("Revenue", rectangle, page)
        sales = page.get_textbox(fitz.Rect(salesRectangle.x0+82,salesRectangle.y0+3,salesRectangle.x0+135,salesRectangle.y1-3)).splitlines()
        print("")
        print(sales)

    earningsRectangle = search_for("Earnings", rectangle, page)
    earnings = page.get_textbox(fitz.Rect(earningsRectangle.x0+82,earningsRectangle.y0+3,earningsRectangle.x0+135,earningsRectangle.y1-3)).splitlines()
    print("")
    print(earnings)


def get_right_text(page: fitz.Page):
    rightText = page.get_textbox(rightRect).splitlines()
    i = 0
    salesHeight = 0
    earningsPerShareHeight = 0
    netProfitHeight = 0

    for line in rightText:
        if line.__contains__("Revenues (") or line.__contains__("Sales ("):
            salesHeight = 215 + i * 9
        if line.__contains__("Earnings per sh"):
            earningsPerShareHeight = 215 + i * 9
        if line.__contains__("Net Profit ("):
            netProfitHeight = 215 + i * 9
        i = i+1

    projectedSalesRect = fitz.Rect(550, salesHeight + 3, 569, salesHeight + 5)
    projectedSales = page.get_textbox(projectedSalesRect).splitlines()

    salesRect = fitz.Rect(310, salesHeight + 3, 430, salesHeight + 5)
    sales = page.get_textbox(salesRect).splitlines()

    earningsPerShareRect = fitz.Rect(310, earningsPerShareHeight + 3, 430, earningsPerShareHeight + 5)
    earningsPerShare = page.get_textbox(earningsPerShareRect).splitlines() 

    netProfitRect = fitz.Rect(310, netProfitHeight + 3, 430, netProfitHeight + 5)
    netProfit = page.get_textbox(netProfitRect).splitlines()

    print("")
    print("projected sales")
    print(projectedSales)
    print("")
    print("sales")
    print(sales)
    print("")
    print("earnings per share")
    print(earningsPerShare)
    print("")
    print("net profit")
    print(netProfit)

def get_text(page: fitz.Page):
    timelinessText = page.get_textbox(timelinessRect).splitlines() 
    timeliness = int(timelinessText[0])

    safetyText = page.get_textbox(safetyRect).splitlines()
    safety = int(safetyText[0])

    betaText = page.get_textbox(betaRect).splitlines()
    beta = float(betaText[0])

    rating = page.get_textbox(ratingRect).splitlines()

    print("")
    print("temiliness ")
    print(timeliness)

    print("")
    print("safety " )
    print(safety)

    print("")
    print("beta")
    print(beta)

    print("")
    print("rating")
    print(rating[0])

    get_left_text(page, leftRect)
    get_right_text(page)
    

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
timelinessRect = fitz.Rect(88,58,90,60)
safetyRect = fitz.Rect(88,68,90,74) 
betaRect = fitz.Rect(62,91.5,75,97.5) 
ratingRect = fitz.Rect(550,725.5,563,731)
rightRect = fitz.Rect(478,215,540,404)
leftRect = fitz.Rect(45.5,205,188,540)

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
