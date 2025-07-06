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
from typing import List
import fitz

def search_for(text, rectangle: fitz.Rect, page: fitz.Page) -> fitz.Rect:
    foundRectangle = page.search_for(text, clip=rectangle)
    if(foundRectangle.__len__() > 0):
        return foundRectangle[0]
    else:
        return fitz.Rect(0,0,0,0)

def text_millions_to_number(number: str) -> float:
    tmp = number.split()
    if tmp[1].__contains__("bill"):
        return float(tmp[0].replace(",",""))
    elif tmp[1].__contains__("mill"):
        return float(tmp[0].replace(",",""))/1000
    elif tmp[1].__contains__("trill"):
        return float(tmp[0].replace(",",""))*1000
    return 0

def get_left_text(page: fitz.Page, rectangle: fitz.Rect) -> tuple[float, float, List[str], List[str], List[str], List[str], fitz.Rect, fitz.Rect, fitz.Rect, fitz.Rect]:
    debtRectangle = search_for("Total Debt", rectangle, page)
    debtRaw = page.get_textbox(fitz.Rect(debtRectangle.x1,debtRectangle.y0,debtRectangle.x1+35,debtRectangle.y1)).splitlines()
    debt = debtRaw[0].split("$")[1]
    debt = text_millions_to_number(debt)

    marketCapRectangle = search_for("MARKET CAP", rectangle, page)
    marketCapRaw = page.get_textbox(fitz.Rect(marketCapRectangle.x1+3,marketCapRectangle.y0,marketCapRectangle.x1+35,marketCapRectangle.y1)).splitlines()
    marketCap = marketCapRaw[0].split("$")[1]
    marketCap = text_millions_to_number(marketCap)

    salesGrowth = []
    salesRectangle = search_for("Sales", rectangle, page)
    if salesRectangle != fitz.Rect(0,0,0,0):
        salesGrowth = page.get_textbox(fitz.Rect(salesRectangle.x0+82,salesRectangle.y0+3,salesRectangle.x0+135,salesRectangle.y1-3)).splitlines()
    else:
        salesRectangle = search_for("Revenue", rectangle, page)
        salesGrowth = page.get_textbox(fitz.Rect(salesRectangle.x0+82,salesRectangle.y0+3,salesRectangle.x0+135,salesRectangle.y1-3)).splitlines()

    earningsRectangle = search_for("Earnings", rectangle, page)
    earningsGrowth = page.get_textbox(fitz.Rect(earningsRectangle.x0+82,earningsRectangle.y0+3,earningsRectangle.x0+135,earningsRectangle.y1-3)).splitlines()
    return (debt, marketCap, salesGrowth, earningsGrowth, debtRaw, marketCapRaw, debtRectangle, marketCapRectangle, salesRectangle, earningsRectangle)

def consecutive_growth(list: List[str]) -> int:
    lenght = len(list)
    previous = float(list[lenght-1].lstrip("d"))
    growth = 0
    for i in range(len(list)-2, -1, -1):
        current = float(list[i].lstrip("d"))
        if current < previous:
            previous = current 
            growth = growth + 1; 
        else:
            break
    return growth


def get_right_text(page: fitz.Page) -> tuple[str, int, int, int, List[str], List[str], List[str], List[str], fitz.Rect, fitz.Rect, fitz.Rect, fitz.Rect]:
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
    projectedSalesRaw = page.get_textbox(projectedSalesRect).splitlines()
    projectedSales = projectedSalesRaw[0]

    salesRect = fitz.Rect(310, salesHeight + 3, 430, salesHeight + 5)
    salesRaw = page.get_textbox(salesRect).splitlines()
    salesConsecutiveGrowth = consecutive_growth(salesRaw)

    earningsPerShareRect = fitz.Rect(310, earningsPerShareHeight + 3, 430, earningsPerShareHeight + 5)
    earningsPerShareRaw = page.get_textbox(earningsPerShareRect).splitlines() 
    earningsPerShareConsecutiveGrowth = consecutive_growth(earningsPerShareRaw)

    netProfitRect = fitz.Rect(310, netProfitHeight + 3, 430, netProfitHeight + 5)
    netProfitRaw = page.get_textbox(netProfitRect).splitlines()
    netProfitConsecutiveGrowth = consecutive_growth(netProfitRaw)

    return (projectedSales, salesConsecutiveGrowth, earningsPerShareConsecutiveGrowth, netProfitConsecutiveGrowth, projectedSalesRaw,salesRaw, earningsPerShareRaw, netProfitRaw, projectedSalesRect, salesRect,earningsPerShareRect,netProfitRect)

    # print("")
    # print("projected sales")
    # print(projectedSales)
    # print("")
    # print("sales")
    # print(consecutive_growth(sales))
    # print(sales)
    # print("")
    # print("earnings per share")
    # print(consecutive_growth(earningsPerShare))
    # print(earningsPerShare)
    # print("")
    # print("net profit")
    # print(consecutive_growth(netProfit))
    # print(netProfit)


def get_text(page: fitz.Page):
    timelinessText = page.get_textbox(timelinessRect).splitlines()
    timeliness = timelinessText[0].lstrip().rstrip()

    safetyText = page.get_textbox(safetyRect).splitlines()
    safety = safetyText[0].lstrip().rstrip()

    betaText = page.get_textbox(betaRect).splitlines()
    beta = betaText[0].lstrip().rstrip()

    ratingText = page.get_textbox(ratingRect).splitlines()
    rating = ratingText[0].lstrip().rstrip()

    (debt, marketCap, salesGrowth, earningsGrowth, debtRaw, marketCapRaw, debtRectangle, marketCapRectangle, salesRectangle, earningsRectangle) = get_left_text(page, leftRect)
    (projectedSales, salesConsecutiveGrowth, earningsPerShareConsecutiveGrowth, netProfitConsecutiveGrowth, projectedSalesRaw,salesRaw, earningsPerShareRaw, netProfitRaw, projectedSalesRect, salesRect,earningsPerShareRect,netProfitRect) = get_right_text(page)

    print("")
    print("Q2  - timeliness ")
    print(timeliness)
    print(timelinessText)

    print("")
    print("Q3  - safety " )
    print(safety)
    print(safetyText)

    print("")
    print("Q4a - debt ")
    print(debt)
    print(debtRaw)

    print("")
    print("Q4b - market cap ")
    print(marketCap)
    print(marketCapRaw)

    print("")
    print("Q5  - beta")
    print(beta)
    print(betaText)

    print("")
    print("Q6a - %growth in sales last 5 years")
    print(salesGrowth[0])
    print(salesGrowth)

    print("")
    print("Q6b - years of consecutive sales growth")
    print(salesConsecutiveGrowth)
    print(salesRaw)

    print("")
    print("Q6c - %growth in earnings last 5 years")
    print(earningsGrowth[0])
    print(earningsGrowth)

    print("")
    print("Q6d - years of consecutive earnings growth")
    print(earningsPerShareConsecutiveGrowth)
    print(earningsPerShareRaw)

    print("")
    print("Q6e - projected sales")
    print(projectedSales)
    print(projectedSalesRaw)

    print("")
    print("Q6f - %projected growth in sales")
    print(salesGrowth[1])
    print(salesGrowth)

    print("")
    print("Q6g - %projected growth in earnings")
    print(earningsGrowth[1])
    print(earningsGrowth)

    print("")
    print("Q7a - consecutive net profit growth")
    print(netProfitConsecutiveGrowth)
    print(netProfitRaw)

    print("")
    print("Q8  - rating")
    print(rating)
    print(ratingText)

    

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
print("ABERCROMBIE:")
get_text(page3)
