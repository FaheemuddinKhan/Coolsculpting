import scrapy
import pprint
import csv
import os
import json
from ..items import CoolsculptingItem


class CoolsculptingspiderSpider(scrapy.Spider):
    name = 'coolsculptingspider'

    def start_requests(self):
        start_url = 'https://find.coolsculpting.com/find-a-center/'
        yield scrapy.Request(start_url, self.parse)

    def parse(self, response):
        cvToken = response.xpath('//*[@id="master"]/main/div[1]/input[3]').attrib['value']

        headers = scrapy.http.headers.Headers({
            "__customVerificationToken": cvToken,
            "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "find.coolsculpting.com",
        "Pragma": "no-cache",
        "sec-ch-ua": 'Google Chrome;v="87","Not;A Brand";v="99","Chromium";v="87"',
        "sec-ch-ua-mobile":"?0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",})
        cwd = os.getcwd()
        path = os.path.join(cwd+"/zip-codes-database-FREE.csv")
        print(path)
        with open(path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                zipCode = row[0]
                request_url = f"https://find.coolsculpting.com/api/FindProviders?ProductId=35&MileRadius=50&SortBy=3&PerPage=100&PageNum=1&ZipCode={zipCode}&Latitude=0&Longitude=0&_token=" + cvToken
                yield scrapy.Request(request_url,headers=headers, callback=self.parse_data)


    def parse_data(self, response):
        item = CoolsculptingItem()
        print("RESPONSE DATA BODY STARTS")
        print(json.loads(response.body))
        print("RESPONSE DATA BODY ENDS")
        try:
            data = json.loads(response.body)['Data']
            accounts = data["Accounts"]
            for account in accounts:
                print(account)
                item["Id"] = account["ShiptoBioId"]
                item["Name"] = account["DisplayName"]
                item["City"] = account["City"]
                item["State"] = account["State"]
                item["Email"] = account["EmailAddress"]
                item["Telephone"] = account["TelephoneNumber"]
                item["Website"] = account["WebsiteUrl"]
                yield item
        except Exception as e:
            print(e)
