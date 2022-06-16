# remove duplicate link scraping
import scrapy
# from ..items import MoneycontrolItem
from moneycontrol.items import MoneycontrolItem
import pandas as pd
import numpy as np

class ExampleSpider(scrapy.Spider):
	name = 'moneycontrol'
	allowed_domains = ['moneycontrol.com'] # comment this if error
	start_urls = ['https://www.moneycontrol.com/india/stockpricequote/']

	def parse(self, response):
		if response.css("table.pcq_tbl.MT10 a::attr(href)").getall():
			all_stock_name_list = response.css("table a::text").getall()
			all_stock_link_list = response.css("table.pcq_tbl.MT10 a::attr(href)").getall()
			all_stock_zip = zip(all_stock_name_list, all_stock_link_list)
			all_stock_dict = {}

			for a,b in all_stock_zip:
				all_stock_dict[a] = b
			
			mystock_df = pd.read_csv('fetch_stock_name_list.csv')
			mystock_list = mystock_df['stock_name'].tolist()

			mystock_dict = {}

			for i in mystock_list:
				mystock_dict[i] = all_stock_dict[i] 

			global links_to_scrap
			links_to_scrap = list(mystock_dict.values())		

		# if response.css("h1.pcstname::text").get():
		# stock_name =  response.css("h1.pcstname::text").get()
		# bse_price, nse_price = response.css("span.span_price_wrap.stprh::text").getall()
		stock_name = response.css("div.stkname::text").extract()
		bse_price = response.css("div.pcstkspr.nsestkcp.bsestkcp.futstkcp.optstkcp::text").extract()
		item = MoneycontrolItem()
		item['stock_name'] = stock_name
		item['bse_price'] = bse_price
		# item['nse_price'] = nse_price
		print(f"{stock_name} {bse_price}")
		yield item

		for link in links_to_scrap:
			if link is not None:
				if not link.startswith("https://moneycontrol.com/"):
					page_url = ("https://moneycontrol.com/" + link)
				next_page = response.urljoin(page_url)
				yield response.follow(next_page, callback=self.parse)
