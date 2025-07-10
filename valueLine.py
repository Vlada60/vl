from os import P_ALL
from typing import List
import vlTypes
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

def get_left_text(page: fitz.Page, debtRect: fitz.Rect, marketCapRect: fitz.Rect, salesRect: fitz.Rect, earningsRect) -> tuple[float, float, List[str], List[str], List[str], List[str]]:
    debtRaw = page.get_textbox(debtRect).splitlines()
    try:
        debt = debtRaw[0].split("$")[1]
        debt = text_millions_to_number(debt)
    except:
        print("\033[91mError:\033[0m Debt was not able to be extracted")
        debt = -1

    marketCapRaw = page.get_textbox(marketCapRect).splitlines()
    try:
        marketCap = marketCapRaw[0].split("$")[1]
        marketCap = text_millions_to_number(marketCap)
    except:
        print("\033[91mError:\033[0m Market Cap was not able to be extracted")
        marketCap = -1

    salesGrowth = []
    salesGrowth = page.get_textbox(salesRect).splitlines()

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

    earningsGrowth = page.get_textbox(earningsRect).splitlines()

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

    return (debt, marketCap, salesGrowth, earningsGrowth, debtRaw, marketCapRaw)

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


def get_right_text(page: fitz.Page, projectedSalesRect: fitz.Rect, projectedEarningsPSRect: fitz.Rect, salesRect: fitz.Rect, earningsPerShareRect: fitz.Rect, netProfitRect: fitz.Rect, bookValuePerSHRect: fitz.Rect, avgAnnualPERect: fitz.Rect) -> tuple[str, int, int, int, str, str, list[str], list[str], list[str], list[str], list[str], list[str], list[str]]:
    projectedSalesRaw = page.get_textbox(projectedSalesRect).splitlines()
    try:
        projectedSales = projectedSalesRaw[0].lstrip().rstrip()
    except:
        print("\033[91mError:\033[0m Debt was not able to be extracted")
        projectedSales = "error"
        
    projectedEarningsPSRaw = page.get_textbox(projectedEarningsPSRect).splitlines()
    try:
        projectedEarningsPS = projectedEarningsPSRaw[0].lstrip().rstrip()
    except:
        print("\033[91mError:\033[0m Projected earnings per share was not able to be extracted")
        projectedEarningsPS = "error"

    salesRaw = page.get_textbox(salesRect).splitlines()
    salesConsecutiveGrowth = consecutive_growth(salesRaw)
        
    earningsPerShareRaw = page.get_textbox(earningsPerShareRect).splitlines() 
    earningsPerShareConsecutiveGrowth = consecutive_growth(earningsPerShareRaw)

    netProfitRaw = page.get_textbox(netProfitRect).splitlines()
    netProfitConsecutiveGrowth = consecutive_growth(netProfitRaw)

    bookValuePerSHRaw = page.get_textbox(bookValuePerSHRect).splitlines()
    try:
        bookValuePerSH = bookValuePerSHRaw[0].lstrip().rstrip()
    except:
        print("\033[91mError:\033[0m Debt was not able to be extracted")
        bookValuePerSH = "error"

    avgAnnualPE = page.get_textbox(avgAnnualPERect).splitlines()

    return (projectedSales, salesConsecutiveGrowth, earningsPerShareConsecutiveGrowth, netProfitConsecutiveGrowth, projectedEarningsPS, bookValuePerSH, avgAnnualPE, projectedSalesRaw,salesRaw, earningsPerShareRaw, netProfitRaw, projectedEarningsPSRaw, bookValuePerSHRaw)

def get_top_text(page: fitz.Page, highPriceRect: fitz.Rect, lowPriceRect: fitz.Rect) -> tuple[str, list[str], list[str], list[str]]:
    peRaw = page.get_textbox(peRect).splitlines()
    try:
        pe = peRaw[0].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m P/E ratio was not able to be extracted")
        pe = "error"

    highPrice = page.get_textbox(highPriceRect).splitlines()
    lowPrice = page.get_textbox(lowPriceRect).splitlines()

    return (pe, peRaw, highPrice, lowPrice)

def get_top_left_text(page: fitz.Page) -> tuple[str, str, str, str, str, list[str], list[str] ,list[str], list[str], list[str]]:
    timelinessRaw = page.get_textbox(timelinessRect).splitlines()
    try:
        timeliness = timelinessRaw[0].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m timeliness was not able to be extracted")
        timeliness = "error"

    safetyRaw = page.get_textbox(safetyRect).splitlines()
    try:
        safety = safetyRaw[0].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m safety was not able to be extracted")
        safety = "error"

    betaRaw = page.get_textbox(betaRect).splitlines()
    try:
        beta = betaRaw[0].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m beta was not able to be extracted")
        beta = "error"

    ratingRaw = page.get_textbox(ratingRect).splitlines()
    try:
        rating = ratingRaw[0].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m rating was not able to be extracted")
        rating = "error"

    anlTotalReturn = page.get_textbox(anlTotalReturnRect).splitlines()
    try:
        anlTotalReturn = anlTotalReturn[0].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m Annual Total Return was not able to be extracted")
        anlTotalReturn = "error"

    priceProjection = page.get_textbox(priceProjectionRect).splitlines()
    try:
        priceProjection[0] = priceProjection[0].lstrip().rstrip()
        priceProjection[1] = priceProjection[1].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m Price Projection was not able to be extracted")
        priceProjection = ["error", "error"]

    return (timeliness, safety, beta, rating, anlTotalReturn, priceProjection, timelinessRaw, safetyRaw, betaRaw, ratingRaw)

def get_bottom_left(page: fitz.Page, earningsPSFYRect: fitz.Rect ,quarterlyDividentsRect: fitz.Rect, hasDividents: bool):
    earningsPSFYRaw = page.get_textbox(earningsPSFYRect).splitlines()
    try:
        earningsPSFY = earningsPSFYRaw[0].lstrip().rstrip()
    except IndexError:
        print("\033[91mError:\033[0m Earnings per share in the last fiscal year was not able to be extracted")
        earningsPSFY = "error"

    quarterlyDividentsRaw = 0;
    if hasDividents:
        quarterlyDividentsRaw = page.get_textbox(quarterlyDividentsRect).splitlines()
        try:
            quarterlyDividents = quarterlyDividentsRaw[0].lstrip().rstrip()
        except IndexError:
            print("\033[91mError:\033[0m quarterly dividents was not able to be extracted")
            quarterlyDividents = "error"
    else: quarterlyDividents = 0

    return (earningsPSFY, quarterlyDividents, earningsPSFYRaw, quarterlyDividentsRaw)

def add_text_annot_above(text: str, rect: fitz.Rect, page: fitz.Page):
    page.add_freetext_annot(fitz.Rect(rect.x0, rect.y0 - 6, rect.x1 + 10, rect.y0 - 1), text, text_color=(1,0,0),fontsize=6,fill_color=(1,1,1))

def add_text_annot_below(text: str, rect: fitz.Rect, page: fitz.Page):
    page.add_freetext_annot(fitz.Rect(rect.x0, rect.y1 + 1, rect.x1 + 10, rect.y1 + 6), text, text_color=(1,0,0),fontsize=6,fill_color=(1,1,1))

def get_rectangles(page: fitz.Page) -> tuple[fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,fitz.Rect,bool]:
    salesHeight = search_for("Revenues (", rightRect, page)
    if salesHeight == fitz.Rect(0,0,0,0):
        salesHeight = search_for("Sales (", rightRect, page)
    earningsPerShareHeight = search_for("Earnings per sh", rightRect, page)
    netProfitHeight = search_for("Net Profit (", rightRect, page)
    bookValuePSHeight = search_for("Book Value per sh", rightRect, page) 
    avgAnnualPEHeight = search_for("Avg Ann’l P/E Ratio", rightRect, page) 

    projectedSalesRect = fitz.Rect(550, salesHeight.y0, 569, salesHeight.y1)
    salesRect = fitz.Rect(310, salesHeight.y0, 430, salesHeight.y1)
    projectedEarningsPSRect = fitz.Rect(550, earningsPerShareHeight.y0, 569, earningsPerShareHeight.y1)
    earningsPerShareRect = fitz.Rect(310, earningsPerShareHeight.y0, 430, earningsPerShareHeight.y1)
    netProfitRect = fitz.Rect(310, netProfitHeight.y0, 430, netProfitHeight.y1)
    bookValuePSRect = fitz.Rect(405, bookValuePSHeight.y0, 430, bookValuePSHeight.y1)
    avgAnnualPERect = fitz.Rect(310, avgAnnualPEHeight.y0, 430, avgAnnualPEHeight.y1)

    debtRect = search_for("Total Debt", leftRect, page)
    debtRect = fitz.Rect(debtRect.x1,debtRect.y0,debtRect.x1+35,debtRect.y1)
    marketCapRect = search_for("MARKET CAP", leftRect, page)
    marketCapRect = fitz.Rect(marketCapRect.x1+3,marketCapRect.y0,marketCapRect.x1+35,marketCapRect.y1)
    earningsRect = search_for("Earnings", leftRect, page)
    earningsRect = fitz.Rect(earningsRect.x0+82,earningsRect.y0+2,earningsRect.x0+135,earningsRect.y1-3)
    salesGrowthRect = search_for("Sales", leftRect, page)
    if salesGrowthRect != fitz.Rect(0,0,0,0):
        salesGrowthRect = fitz.Rect(salesGrowthRect.x0+82,salesGrowthRect.y0+2,salesGrowthRect.x0+135,salesGrowthRect.y1-3)
    else:
        salesGrowthRect = search_for("Revenue", leftRect, page)
        salesGrowthRect = fitz.Rect(salesGrowthRect.x0+82,salesGrowthRect.y0+2,salesGrowthRect.x0+135,salesGrowthRect.y1-3)

    highPriceRect = search_for("High:", topRect, page) 
    highPriceRect = fitz.Rect(312, highPriceRect.y0, 427, highPriceRect.y1)
    lowPriceRect = fitz.Rect(highPriceRect.x0,highPriceRect.y1 + 2,highPriceRect.x1,highPriceRect.y1 + 6)

    earningsPerShareTextRect = search_for("EARNINGS PER SHARE", bottomLeftRect, page)
    earningsPSFYRect = fitz.Rect(165, earningsPerShareTextRect.y1 + 36, 188, earningsPerShareTextRect.y1 + 40)

    quarterlyDividentsTextRect = search_for("QUARTERLY DIVIDENDS PAID", bottomLeftRect, page)
    quarterlyDividentsRect = fitz.Rect(165, quarterlyDividentsTextRect.y1 + 36, 188, quarterlyDividentsTextRect.y1 + 40)
    
    hasDividents = search_for("NO CASH DIVIDENDS", fitz.Rect(70,180,165,722), page) == fitz.Rect(0,0,0,0)
    
    return (projectedSalesRect, salesRect, earningsPerShareRect,netProfitRect, debtRect, marketCapRect, earningsRect, salesGrowthRect, highPriceRect, lowPriceRect, projectedEarningsPSRect, bookValuePSRect, avgAnnualPERect, earningsPSFYRect, quarterlyDividentsRect, hasDividents)

def get_data(page: fitz.Page) -> tuple[vlTypes.Quallity, vlTypes.Price]:
    (timeliness, safety, beta, rating, anlTotalReturn, priceProjection, timelinessRaw, safetyRaw, betaRaw, ratingRaw) = get_top_left_text(page)
    (projectedSalesRect, salesRect, earningsPerShareRect,netProfitRect, debtRect, marketCapRect, earningsRect, salesGrowthRect, highPriceRect, lowPriceRect, projectedEarningsPSRect, bookValuePSRect, avgAnnualPERect, earningsPSFYRect, quarterlyDividentsRect, hasDividents) = get_rectangles(page)
    (debt, marketCap, salesGrowth, earningsGrowth, debtRaw, marketCapRaw) = get_left_text(page, debtRect, marketCapRect, salesGrowthRect, earningsRect)
    (projectedSales, salesConsecutiveGrowth, earningsPerShareConsecutiveGrowth, netProfitConsecutiveGrowth, projectedEarningsPS, bookValuePerSH, avgAnnualPE, projectedSalesRaw, salesRaw, earningsPerShareRaw, netProfitRaw, projectedEarningsPSRaw, bookValuePerSHRaw) = get_right_text(page, projectedSalesRect, projectedEarningsPSRect, salesRect, earningsPerShareRect, netProfitRect, bookValuePSRect, avgAnnualPERect)
    (pe, peRaw, highPrice,  lowPrice) = get_top_text(page, highPriceRect, lowPriceRect)
    (earningsPSFY, quarterlyDividents, earningsPSFYRaw, quarterlyDividentsRaw) = get_bottom_left(page, earningsPSFYRect, quarterlyDividentsRect , hasDividents)

    for i in range(5):
        try:
            avgAnnualPE[i]
        except IndexError:
            avgAnnualPE.append("error")


    print("")
    print("Q2  - timeliness ")
    print(timeliness)
    print(timelinessRaw)
    page.add_highlight_annot(timelinessRect)
    add_text_annot_above(timeliness,timelinessRect,page)

    print("")
    print("Q3  - safety " )
    print(safety)
    print(safetyRaw)
    page.add_highlight_annot(safetyRect)
    add_text_annot_above(safety,safetyRect,page)

    print("")
    print("Q4a - debt ")
    print(debt)
    print(debtRaw)
    try:
        page.add_highlight_annot(debtRect)
    except ValueError:
        print("\033[91mError:\033[0m Debt Rectangle is invalid, debt was probably not found")
    add_text_annot_above(str(debt) + " bill",debtRect,page)

    print("")
    print("Q4b - market cap ")
    print(marketCap)
    print(marketCapRaw)
    try:
        page.add_highlight_annot(marketCapRect)
    except ValueError:
        print("\033[91mError:\033[0m Market Cap Rectangle is invalid, market cap was probably not found")
    add_text_annot_above(str(marketCap) + " bill",marketCapRect,page)

    print("")
    print("Q5  - beta")
    print(beta)
    print(betaRaw)
    page.add_highlight_annot(betaRect)
    add_text_annot_above(beta, betaRect, page)

    print("")
    print("Q6a - %growth in sales last 5 years")
    print(salesGrowth[0])
    print(salesGrowth)
    try:
        page.add_highlight_annot(salesGrowthRect)
    except ValueError:
        print("\033[91mError:\033[0m Sales Growth Rectangle is invalid, sales growth was probably not found")
    add_text_annot_above(salesGrowth[0], salesGrowthRect, page)

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
        page.add_highlight_annot(earningsRect)
    except ValueError:
        print("\033[91mError:\033[0m Earnings Growth Rectangle is invalid, earnings growth was probably not found")
    add_text_annot_above(earningsGrowth[0], earningsRect, page)

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
    page.add_line_annot(fitz.Point(earningsPerShareRect.x1, earningsPerShareRect.y1),fitz.Point(earningsPerShareRect.x1 + 130, earningsPerShareRect.y1))

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
    add_text_annot_above(salesGrowth[1], fitz.Rect(salesGrowthRect.x0 + 30,salesGrowthRect.y0,salesGrowthRect.x1 + 30,salesGrowthRect.y1), page)

    print("")
    print("Q6g - %projected growth in earnings")
    print(earningsGrowth[1])
    print(earningsGrowth)
    add_text_annot_above(earningsGrowth[1], fitz.Rect(earningsRect.x0 + 30,earningsRect.y0,earningsRect.x1 + 30,earningsRect.y1), page)

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
    print(ratingRaw)
    page.add_highlight_annot(ratingRect)
    add_text_annot_above(rating, ratingRect, page)

    print("")
    print("P2A  - earnings per share last year")
    print(earningsPSFY)
    print(earningsPSFYRaw)
    page.add_highlight_annot(earningsPSFYRect)
    add_text_annot_above(earningsPSFY, earningsPSFYRect, page)

    print("")
    print("P3A - dividents last year")
    print(quarterlyDividents)
    print(quarterlyDividentsRaw)
    if hasDividents:
        page.add_highlight_annot(quarterlyDividentsRect)
    add_text_annot_above(str(quarterlyDividents), quarterlyDividentsRect, page)

    print("")
    print("P3a - Annual projected total high return")
    print(anlTotalReturn)
    page.add_highlight_annot(anlTotalReturnRect)
    add_text_annot_above(anlTotalReturn, anlTotalReturnRect, page)

    print("")
    print("P5a - Avrage annual P/E ratio")
    print(avgAnnualPE)
    try:
        page.add_highlight_annot(avgAnnualPERect)
    except ValueError:
        print("\033[91mError:\033[0m Avrage annual p/e ratio rectangle is invalid, avrage annual p/e ratio is probably not found")
    add_text_annot_above(str(avgAnnualPE), avgAnnualPERect, page)

    print("")
    print("P5b - current P/E ratio")
    print(pe)
    print(peRaw)
    page.add_highlight_annot(peRect)
    add_text_annot_above(pe, peRect, page)

    print("")
    print("P6a - high and low price over 5 years")
    print(highPrice)
    print(lowPrice)
    try:
        page.add_highlight_annot(highPriceRect)
        page.add_highlight_annot(lowPriceRect)
    except ValueError:
        print("\033[91mError:\033[0m High Price Rectangle is invalid, high and low prices were probably not found")
    add_text_annot_above(str(highPrice), highPriceRect, page)
    add_text_annot_below(str(lowPrice), lowPriceRect, page)

    print("")
    print("P6c - Projected earnings per share")
    print(projectedEarningsPS)
    print(projectedEarningsPSRaw)
    try:
        page.add_highlight_annot(projectedEarningsPSRect)
    except ValueError:
        print("\033[91mError:\033[0m Projected earnings per share Rectangle is invalid, projected earnings per share was probably not found")
    add_text_annot_above(projectedEarningsPS, projectedEarningsPSRect, page)

    print("")
    print("P6f - high and low price projection")
    print(priceProjection[0])
    print(priceProjection[1])
    print(priceProjection)
    page.add_highlight_annot(priceProjectionRect)
    add_text_annot_above(priceProjection[0], priceProjectionRect, page)
    add_text_annot_below(priceProjection[1], priceProjectionRect, page)

    print("")
    print("P8 - Book Value per sh")
    print(bookValuePerSH)
    print(bookValuePerSHRaw)
    try:
        page.add_highlight_annot(bookValuePSRect)
    except ValueError:
        print("\033[91mError:\033[0m Book value per share rectangle is invalid, book value per share was probably not found")
    add_text_annot_above(bookValuePerSH, bookValuePSRect, page)

    quality = vlTypes.Quallity(timeliness, safety, debt, marketCap, beta, salesGrowth[0], salesConsecutiveGrowth, earningsGrowth[0], earningsPerShareConsecutiveGrowth, projectedSales, salesGrowth[1], earningsGrowth[1], netProfitConsecutiveGrowth, "", rating)

    price = vlTypes.Price("", earningsPSFY, quarterlyDividents, anlTotalReturn, salesGrowth[0], earningsGrowth[0], salesGrowth[1], earningsGrowth[1], avgAnnualPE, pe, [highPrice, lowPrice], earningsPerShareRaw, projectedEarningsPS, priceProjection, bookValuePerSH)

    return (quality, price)

    
timelinessRect = fitz.Rect(88,55,90,60)
safetyRect = fitz.Rect(88,68,90,74) 
betaRect = fitz.Rect(62,91.5,75,97.5) 
ratingRect = fitz.Rect(550,725.5,563,731)
rightRect = fitz.Rect(478,215,540,404)
leftRect = fitz.Rect(45.5,205,188,540)
peRect = fitz.Rect(311,31,338,49)
topRect = fitz.Rect(141,53,308,62)
anlTotalReturnRect = fitz.Rect(115,155,135,157)
priceProjectionRect = fitz.Rect(64, 155, 80, 165)
bottomLeftRect = fitz.Rect(68, 590, 165, 690)
