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
    debtRectangle = fitz.Rect(debtRectangle.x1,debtRectangle.y0,debtRectangle.x1+35,debtRectangle.y1)
    debtRaw = page.get_textbox(debtRectangle).splitlines()
    try:
        debt = debtRaw[0].split("$")[1]
    except:
        print("\033[91mError:\033[0m Debt was not able to be extracted")
        debt = "error error"
    debt = text_millions_to_number(debt)

    marketCapRectangle = search_for("MARKET CAP", rectangle, page)
    marketCapRectangle = fitz.Rect(marketCapRectangle.x1+3,marketCapRectangle.y0,marketCapRectangle.x1+35,marketCapRectangle.y1)
    marketCapRaw = page.get_textbox(marketCapRectangle).splitlines()
    try:
        marketCap = marketCapRaw[0].split("$")[1]
    except:
        print("\033[91mError:\033[0m Market Cap was not able to be extracted")
        marketCap = "error error"
    marketCap = text_millions_to_number(marketCap)

    salesGrowth = []
    salesRectangle = search_for("Sales", rectangle, page)
    if salesRectangle != fitz.Rect(0,0,0,0):
        salesRectangle = fitz.Rect(salesRectangle.x0+82,salesRectangle.y0+2,salesRectangle.x0+135,salesRectangle.y1-3)
        salesGrowth = page.get_textbox(salesRectangle).splitlines()
    else:
        salesRectangle = search_for("Revenue", rectangle, page)
        salesRectangle = fitz.Rect(salesRectangle.x0+82,salesRectangle.y0+2,salesRectangle.x0+135,salesRectangle.y1-3)
        salesGrowth = page.get_textbox(salesRectangle).splitlines()

    try :
        salesGrowth[0]
    except IndexError:
        print("\033[91mError:\033[0m Sales growth not found")
        salesGrowth = ["error","error"]
    try :
        salesGrowth[1]
    except IndexError:
        print("\033[91mError:\033[0m Sales growth prediction not found")
        salesGrowth[1] = "error"

    earningsRectangle = search_for("Earnings", rectangle, page)
    earningsRectangle = fitz.Rect(earningsRectangle.x0+82,earningsRectangle.y0+2,earningsRectangle.x0+135,earningsRectangle.y1-3)
    earningsGrowth = page.get_textbox(earningsRectangle).splitlines()

    try :
        earningsGrowth[0]
    except IndexError:
        print("\033[91mError:\033[0m Earnigns growth not found")
        earningsGrowth = ["error","error"]
    try :
        earningsGrowth[1]
    except IndexError:
        print("\033[91mError:\033[0m Earnings Growth prediction not found")
        earningsGrowth[1] = "error"

    return (debt, marketCap, salesGrowth, earningsGrowth, debtRaw, marketCapRaw, debtRectangle, marketCapRectangle, salesRectangle, earningsRectangle)

def consecutive_growth(list: List[str]) -> int:
    lenght = len(list)
    try:
        previous = float(list[lenght-1].lstrip("d"))
    except IndexError:
        print("\033[91mError:\033[0m Cannot calculate consecutive growth, the input list is empty")
        return -1
    growth = 0
    for i in range(len(list)-2, -1, -1):
        try:
            current = float(list[i].lstrip("d"))
        except ValueError:
            print("\033[91mError:\033[0m Cannot calculate consecutive growth, the number imput is invalid and probably contains letters")
            return -1
        if current < previous:
            previous = current 
            growth = growth + 1; 
        else:
            break
    return growth


def get_right_text(page: fitz.Page) -> tuple[str, int, int, int, List[str], List[str], List[str], List[str], fitz.Rect, fitz.Rect, fitz.Rect, fitz.Rect]:
    salesHeight = search_for("Revenues (", rightRect, page)
    if salesHeight == fitz.Rect(0,0,0,0):
        salesHeight = search_for("Sales (", rightRect, page)
    earningsPerShareHeight = search_for("Earnings per sh", rightRect, page)
    netProfitHeight = search_for("Net Profit (", rightRect, page)

    projectedSalesRect = fitz.Rect(550, salesHeight.y0, 569, salesHeight.y1)
    projectedSalesRaw = page.get_textbox(projectedSalesRect).splitlines()
    try:
        projectedSales = projectedSalesRaw[0]
    except:
        print("\033[91mError:\033[0m Debt was not able to be extracted")
        projectedSales = "error"

    salesRect = fitz.Rect(310, salesHeight.y0, 430, salesHeight.y1)
    salesRaw = page.get_textbox(salesRect).splitlines()
    salesConsecutiveGrowth = consecutive_growth(salesRaw)

    earningsPerShareRect = fitz.Rect(310, earningsPerShareHeight.y0, 430, earningsPerShareHeight.y1)
    earningsPerShareRaw = page.get_textbox(earningsPerShareRect).splitlines() 
    earningsPerShareConsecutiveGrowth = consecutive_growth(earningsPerShareRaw)

    netProfitRect = fitz.Rect(310, netProfitHeight.y0, 430, netProfitHeight.y1)
    netProfitRaw = page.get_textbox(netProfitRect).splitlines()
    netProfitConsecutiveGrowth = consecutive_growth(netProfitRaw)

    return (projectedSales, salesConsecutiveGrowth, earningsPerShareConsecutiveGrowth, netProfitConsecutiveGrowth, projectedSalesRaw,salesRaw, earningsPerShareRaw, netProfitRaw, projectedSalesRect, salesRect,earningsPerShareRect,netProfitRect)

def add_text_annot_above(text: str, rect: fitz.Rect, page: fitz.Page):
    page.add_freetext_annot(fitz.Rect(rect.x0, rect.y0 - 6, rect.x1 + 10, rect.y0 - 1), text, text_color=(1,0,0),fontsize=6,fill_color=(1,1,1))

def get_text(page: fitz.Page):
    timelinessText = page.get_textbox(timelinessRect).splitlines()
    try:
        timeliness = timelinessText[0].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m timeliness was not able to be extracted")
        timeliness = "error"

    safetyText = page.get_textbox(safetyRect).splitlines()
    try:
        safety = safetyText[0].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m safety was not able to be extracted")
        safety = "error"

    betaText = page.get_textbox(betaRect).splitlines()
    try:
        beta = betaText[0].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m beta was not able to be extracted")
        beta = "error"

    ratingText = page.get_textbox(ratingRect).splitlines()
    try:
        rating = ratingText[0].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m rating was not able to be extracted")
        rating = "error"

    (debt, marketCap, salesGrowth, earningsGrowth, debtRaw, marketCapRaw, debtRectangle, marketCapRectangle, salesRectangle, earningsRectangle) = get_left_text(page, leftRect)
    (projectedSales, salesConsecutiveGrowth, earningsPerShareConsecutiveGrowth, netProfitConsecutiveGrowth, projectedSalesRaw,salesRaw, earningsPerShareRaw, netProfitRaw, projectedSalesRect, salesRect,earningsPerShareRect,netProfitRect) = get_right_text(page)

    print("")
    print("Q2  - timeliness ")
    print(timeliness)
    print(timelinessText)
    page.add_highlight_annot(timelinessRect)
    add_text_annot_above(timeliness,timelinessRect,page)

    print("")
    print("Q3  - safety " )
    print(safety)
    print(safetyText)
    page.add_highlight_annot(safetyRect)
    add_text_annot_above(safety,safetyRect,page)

    print("")
    print("Q4a - debt ")
    print(debt)
    print(debtRaw)
    try:
        page.add_highlight_annot(debtRectangle)
    except ValueError:
        print("\033[91mError:\033[0m Debt Rectangle is invalid, debt was probably not found")
    add_text_annot_above(str(debt) + " bill",debtRectangle,page)

    print("")
    print("Q4b - market cap ")
    print(marketCap)
    print(marketCapRaw)
    try:
        page.add_highlight_annot(marketCapRectangle)
    except ValueError:
        print("\033[91mError:\033[0m Market Cap Rectangle is invalid, market cap was probably not found")
    add_text_annot_above(str(marketCap) + " bill",marketCapRectangle,page)

    print("")
    print("Q5  - beta")
    print(beta)
    print(betaText)
    page.add_highlight_annot(betaRect)
    add_text_annot_above(beta, betaRect, page)

    print("")
    print("Q6a - %growth in sales last 5 years")
    print(salesGrowth[0])
    print(salesGrowth)
    try:
        page.add_highlight_annot(salesRectangle)
    except ValueError:
        print("\033[91mError:\033[0m Sales Growth Rectangle is invalid, sales growth was probably not found")
    add_text_annot_above(salesGrowth[0], salesRectangle, page)

    print("")
    print("Q6b - years of consecutive sales growth")
    print(salesConsecutiveGrowth)
    print(salesRaw)
    try:
        page.add_highlight_annot(salesRect)
    except ValueError:
        print("\033[91mError:\033[0m Sales Rectangle is invalid, sales was probably not found")
    add_text_annot_above(str(salesRaw),salesRect, page)
    page.add_line_annot(fitz.Point(salesRect.x1 - 25.5 - salesConsecutiveGrowth*24, salesRect.y0),fitz.Point(salesRect.x1 - 25.5 - salesConsecutiveGrowth*24, salesRect.y1 + 10))
    page.add_line_annot(fitz.Point(salesRect.x1, salesRect.y1),fitz.Point(salesRect.x1 + 130, salesRect.y1))

    print("")
    print("Q6c - %growth in earnings last 5 years")
    print(earningsGrowth[0])
    print(earningsGrowth)
    try:
        page.add_highlight_annot(earningsRectangle)
    except ValueError:
        print("\033[91mError:\033[0m Earnings Growth Rectangle is invalid, earnings growth was probably not found")
    add_text_annot_above(earningsGrowth[0], earningsRectangle, page)

    print("")
    print("Q6d - years of consecutive earnings growth")
    print(earningsPerShareConsecutiveGrowth)
    print(earningsPerShareRaw)
    try:
        page.add_highlight_annot(earningsPerShareRect)
    except ValueError:
        print("\033[91mError:\033[0m Earnings per share rectangle is invalid, earnings per share was probably not found")
    add_text_annot_above(str(earningsPerShareRaw),earningsPerShareRect, page)
    page.add_line_annot(fitz.Point(earningsPerShareRect.x1 - 25.5 - earningsPerShareConsecutiveGrowth*24, earningsPerShareRect.y0),fitz.Point(earningsPerShareRect.x1 - 25.5 - earningsPerShareConsecutiveGrowth*24, earningsPerShareRect.y1 + 10))
    page.add_line_annot(fitz.Point(earningsPerShareRect.x1, earningsPerShareRect.y1),fitz.Point(earningsPerShareRect.x1 + 100, earningsPerShareRect.y1))

    print("")
    print("Q6e - projected sales")
    print(projectedSales)
    print(projectedSalesRaw)
    try:
        page.add_highlight_annot(projectedSalesRect)
    except ValueError:
        print("\033[91mError:\033[0m Projected sales rectangle is invalid, projected sales was probably not found")
    add_text_annot_above(projectedSales,projectedSalesRect,page)

    print("")
    print("Q6f - %projected growth in sales")
    print(salesGrowth[1])
    print(salesGrowth)
    add_text_annot_above(salesGrowth[1], fitz.Rect(salesRectangle.x0 + 30,salesRectangle.y0,salesRectangle.x1 + 30,salesRectangle.y1), page)

    print("")
    print("Q6g - %projected growth in earnings")
    print(earningsGrowth[1])
    print(earningsGrowth)
    add_text_annot_above(earningsGrowth[1], fitz.Rect(earningsRectangle.x0 + 30,earningsRectangle.y0,earningsRectangle.x1 + 30,earningsRectangle.y1), page)

    print("")
    print("Q7a - consecutive net profit growth")
    print(netProfitConsecutiveGrowth)
    print(netProfitRaw)
    try:
        page.add_highlight_annot(netProfitRect)
    except ValueError:
        print("\033[91mError:\033[0m Net profit Rectangle is invalid, net profit was probably not found")
    add_text_annot_above(str(netProfitRaw),netProfitRect, page)
    page.add_line_annot(fitz.Point(netProfitRect.x1 - 25.5 - netProfitConsecutiveGrowth*24, netProfitRect.y0),fitz.Point(netProfitRect.x1 - 25.5 - netProfitConsecutiveGrowth*24, netProfitRect.y1 + 10))
    page.add_line_annot(fitz.Point(netProfitRect.x1, netProfitRect.y1),fitz.Point(netProfitRect.x1 + 100, netProfitRect.y1))

    print("")
    print("Q8  - rating")
    print(rating)
    print(ratingText)
    page.add_highlight_annot(ratingRect)
    add_text_annot_above(rating, ratingRect, page)

    

doc1name = "/home/vlada/Desktop/VL KO 2301.pdf"
doc2name = "/home/vlada/Desktop/VL META 2302.pdf"
doc3name = "/home/vlada/Desktop/VL ANF 2301.pdf"

doc1 = fitz.open(doc1name)  # any supported document type
doc2 = fitz.open(doc2name)
doc3 = fitz.open(doc3name)

page1 = doc1[0]
page2 = doc2[0]
page3 = doc3[0]

timelinessRect = fitz.Rect(88,55,90,60)
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

doc1.save(doc1name.rstrip(".pdf") + "-tmp.pdf")
doc2.save(doc2name.rstrip(".pdf") + "-tmp.pdf")
doc3.save(doc3name.rstrip(".pdf") + "-tmp.pdf")
