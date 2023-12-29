import csv
import json
import re
from bs4 import BeautifulSoup as bs
import datetime as dt

class data:
    def __init__(self, page, ticker):
        self.page = page
        self.ticker = ticker.upper()
        self.dtChart = self.page.locator('.results-os-bar-chart')
        self.dtChartBar = self.dtChart.locator('g.recharts-bar:last-child')
        self.dtChartTt = self.page.inner_html('.recharts-tooltip-wrapper')
        self.cashChart = self.page.locator('p:has-text("Cash Position")~p').inner_html()
        self.html = self.page.content()
        # self.s1 = self.page.locator('#results-s1 .result-card-wrapper').inner_html()
        # self.wrt = self.page.locator('id=results-warrant').inner_html()
        # self.con = self.page.locator('id=results-conv-pref').inner_html()
        # self.atm = self.page.locator('id=results-atm').inner_html()
        # self.el = self.page.locator('id=results-equity-line').inner_html()
        # self.shf = self.page.locator('id=results-shelf').inner_html()
        self.filename = './HisData/Dilution.csv'
        self.dtn = dt.datetime.now().strftime("%Y-%m-%d")

    async def getData(self):
        # Defining csv data
        header = [
            'Ticker',
            'Date',
            'Dilution Statement',
            'Cash Statement',
            'S-1',
            'Warrant',
            'Convertible Preferred',
            'ATM',
            'Equity Line',
            'Shelf',
        ]
        data = [self.ticker, self.dtn]

        # write dilution data into the csv
        with open(self.filename, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            
        await self.page.goto(f"https://dilutiontracker.com/app/search/{self.ticker}")
        
        # start of dilution chart
        await self.dtChartBar.hover()
        soup = bs(await self.dtChartTt, "html.parser")
        dtstate = soup.find("p", {"class": "recharts-tooltip-label"}).text
        data.append(dtstate)
        # end of dilution chart

        # start of cash statement
        cfStmt = (await self.cashChart)
        if(re.search(r'(cashflow)', cfStmt, re.A|re.M|re.I)):
            temp = cfStmt.partition("cashflow")[2]
            cfStatus = temp.split(" ")[1]
            cfNum = re.sub(r'(\$|M)', '', re.search(r'\$.*M', temp, re.A|re.M|re.I)[0])
            data.append({"Status": cfStatus, "Detail" : cfNum})
        elif(re.search(r'(of cash left)', cfStmt, re.A|re.M|re.I)):
            soup = bs(cfStmt, "html.parser")
            infos = soup.find_all("strong")
            cPath = ["Cash left", "Cash burn", "Current Cash"]
            cObj = {"Status": "negative", "Cash left": "", "Cash burn": "", "Current Cash": ""}
            for idx, i in enumerate(infos):
                txt = re.sub(r'(\$|M|months| )', "", i.get_text())
                if(txt[-1] == "."):
                    txt = txt[0:-1]
                cObj[cPath[idx]] = txt

        # end of cash statement

        html = bs(await self.html, "html.parser")
        if html:
            # start of s-1 statement
            soup = html.find("div", {"id": "results-s1"}).find("div", {"class": "result-card-wrapper"})
            fieldReg = "S-1 Filing Date|Status|Placement Agent|Final Warrant Coverage|Final Pricing|Final Deal Size|Final Shares Offered|Exercise Price"
            data = getCardsInfo(soup, fieldReg, data)
            # end of s-1 statement

            # start of warrant
            soup = html.find("div", {"id": "results-warrant"})
            fieldReg = "Remaining Warrants|Exercise Price|Total Warrants|Placement agent|Price Protection|Exercisable Date|Expiration Date"
            data = getCardsInfo(soup, fieldReg, data)
            # end of warrant

            # start of convertible preferred
            soup = html.find("div", {"id": "results-conv-pref"})
            fieldReg = "Remaining Shares|Remaining Dollar|Conversion Price|Total Shares|Placement Agent|Convertible Date"
            data = getCardsInfo(soup, fieldReg, data)
            # end of convertible preferred

            # start of atm
            soup = html.find("div", {"id": "results-atm"})
            fieldReg = "Remaining ATM|Total ATM Capacity|Baby Shelf|Remaining Capacity w/o Baby Shelf|Placement Agent|Agreement Start Date|Last Update Date"
            data = getCardsInfo(soup, fieldReg, data)
            # end of atm

            # start of equity line
            soup = html.find("div", {"id": "results-equity-line"})
            fieldReg = "Remaining|Total|Start Date|End Date"
            data = getCardsInfo(soup, fieldReg, data)
            # end of equity line

            # start of shelf
            soup = html.find("div", {"id": "results-shelf"})
            fieldReg = "Raisable Amount|Capacity|Baby Shelf Restriction|Float|IB6 Float Value|Banker|Effect Date|Expiration Date"
            data = getCardsInfo(soup, fieldReg, data)
            # end of shelf
            print(data)

def getCardsInfo(soup, reg, data):
    if(soup != None):
        cards = soup.find_all("div", {"class": "filing_details_card"})
        tgData = []
        for i in cards:
            title = i.find("h5", {"class": "list-group-item-heading"}).get_text()
            status = i.find("p", {"class": "filing-list-group-subheading-text"}).get_text()
            if(not(bool(re.search(r"(cancelled|Depleted|Expired)", title, re.A|re.M|re.I))) & bool(re.search(r"(Registered|Priced)", status, re.A|re.M|re.I))):
                res = i.find_all("span", string=re.compile(reg))
                tempData = {}
                for k in res:
                    label = re.search(rf"{reg}", k.get_text()).group(0)
                    val = k.find_next_siblings("span")[0].get_text()
                    tempData[label] = val
                tgData.append(tempData)
        data.append(tgData)
    else:
        data.append(None)
    return data

# class rating:
    # print("hi")