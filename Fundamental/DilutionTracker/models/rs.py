from bs4 import BeautifulSoup as bs

# Get reverse split data
class ReSplit:
    def __init__(self, page, ticker):
        self.page = page
        self.ticker = ticker.upper()
        self.table = self.page.locator("table").inner_html()

    async def getData(self):
        await self.page.goto("https://dilutiontracker.com/app/reverse-split")
        data = []
        soup = bs(await self.table, "html.parser")
        rows = soup.find_all(lambda tag:tag.name=="tr" and "Upcoming" in tag.text)
        header = ["Ticker", "Effective Date", "Split Ratio", "Float", "Status"]
        for row in rows:
            tempData = {}
            cols = row.find_all("td")
            for idx, col in enumerate(cols):
                if(idx != 3):
                    tempData[header[idx]] = col.get_text()
            data.append(tempData)
        print(data)