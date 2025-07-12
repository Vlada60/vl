from gspread.utils import ValueInputOption
import vlTypes
import gspread

gc = gspread.oauth(credentials_filename="./credentials.json")

def insert_to_sheets(quality: vlTypes.Quallity, price: vlTypes.Price):
    try:
        sheet = gc.open("the sheet")
    except gspread.exceptions.SpreadsheetNotFound:
        sheet = gc.copy("1lBct8NGRyz0lV3qLV-MuE3olsJl_871OibU6ExkoMrE", "the sheet")

    qualityWorksheet = sheet.worksheet("Quality")
    priceWorksheet = sheet.worksheet("Price")

    qualityWorksheet.batch_update([
        {
            'range': 'E14',
            'values': [[quality.q2]]
        },
        {
            'range': 'E18',
            'values': [[quality.q3]]
        },
        {
            'range': 'B25:C26',
            'values': [[quality.q4a, quality.q4b]]
        },
        {
            'range': 'E27',
            'values': [[quality.q5]]
        },
        {
            'range': 'D33',
            'values': [[quality.q6a]]
        },
        {
            'range': 'J38',
            'values': [[quality.q6b]]
        },
        {
            'range': 'D35',
            'values': [[quality.q6c]]
        },
        {
            'range': 'J42',
            'values': [[quality.q6d]]
        },
        {
            'range': 'B45',
            'values': [[quality.q6e]]
        },
        {
            'range': 'D50',
            'values': [[quality.q6f]]
        },
        {
            'range': 'D52',
            'values': [[quality.q6g]]
        },
        {
            'range': 'Q64',
            'values': [[quality.q7[0]]]
        },
        {
            'range': 'B78',
            'values': [[quality.q7[1]]]
        },
        {
            'range': 'C74',
            'values': [[quality.q8]]
        },
    ], value_input_option=ValueInputOption.user_entered)

    text = "9"
    number = "21"
    priceWorksheet.batch_update([
        {
            'range': 'M5:M6',
            'values': [[price.p2a],[price.p2b]]
        },
        {
            'range': 'M10',
            'values': [[price.p3a]]
        },
        {
            'range': 'M20:M25',
            'values': [[price.p5a[0]],[price.p5a[1]],[price.p5a[2]],[price.p5a[3]],[price.p5a[4]]]
        },
        {
            'range': 'M27',
            'values': [[price.p5b]]
        },
        {
            'range': 'E31:Q31',
            'values': [[price.p6a[0][0],"","",price.p6a[0][1],"","",price.p6a[0][2],"","",price.p6a[0][3],"","",price.p6a[0][4]]]
        },
        {
            'range': 'E33:Q33',
            'values': [[price.p6a[1][0],"","",price.p6a[1][1],"","",price.p6a[1][2],"","",price.p6a[1][3],"","",price.p6a[1][4]]]
        },
        {
            'range': 'E35:Q35',
            'values': [[price.p6b[0],"","",price.p6b[1],"","",price.p6b[2],"","",price.p6b[3],"","",price.p6b[4]]]
        },
        {
            'range': 'I38',
            'values': [[price.p6c]]
        },
    ], value_input_option=ValueInputOption.user_entered)


