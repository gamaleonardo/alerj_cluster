# -*- coding: utf-8 -*-
import scrapy
import re

class AlerjAtasSpider(scrapy.Spider):
	name = 'alerj_atas'
	allowed_domains = ['mail.camara.rj.gov.br']
	start_urls = ['https://mail.camara.rj.gov.br/APL/Legislativos/atas.nsf/AtasInt?OpenForm&Start=1&Count=100&Expand=1', 'https://mail.camara.rj.gov.br/APL/Legislativos/atas.nsf/AtasInt?OpenForm&Start=1&Count=100&Expand=2', 'https://mail.camara.rj.gov.br/APL/Legislativos/atas.nsf/AtasInt?OpenForm&Start=1&Count=100&Expand=3', 'https://mail.camara.rj.gov.br/APL/Legislativos/atas.nsf/AtasInt?OpenForm&Start=1&Count=100&Expand=4']
	
	def parse(self, response):
		months_link = response.css('a::attr(href)').extract()
		
		row_data = zip(months_link)
		for item in row_data:
			ata_split = item[0].split('&')
			if len(ata_split) > 1:
				ata_index = ata_split[-1].split('=')[-1]
				if ata_index.find('.') != -1:
					new_url_request = 'https://mail.camara.rj.gov.br' + item[0]
					#set_urls = {
					#	'URL': new_url_request
					#}
					#yield set_urls
					yield scrapy.Request(url=new_url_request, callback=self.parse_ata_link)
			
	def parse_ata_link(self, response):
		
		a_selectors = response.xpath("//a")
		
		for selector in a_selectors:
			title = selector.xpath("text()").extract_first()
			link = selector.xpath("@href").extract_first()
		
			if link is not None and link.find('OpenDocument') != -1:
				csv_data = {
					'ata_link': link,
					'ata_title': title
				}
				yield csv_data
				ata_url = 'https://mail.camara.rj.gov.br' + link
				yield scrapy.Request(url=ata_url,callback=self.parse_ata_document,cb_kwargs=dict(ata_title=title))
				
	def parse_ata_document(self, response, ata_title):
		filename = 'scraped_files/' + ata_title.replace('/', '-') + '.html' #replace slashs to void file name errors
		with open(filename, 'wb') as f:
			f.write(response.body)
