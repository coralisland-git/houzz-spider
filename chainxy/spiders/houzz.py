# from __future__ import unicode_literals
import scrapy
import json
import os
import scrapy
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from chainxy.items import ChainItem
from lxml import etree
from selenium import webdriver
from lxml import html
import pdb
import time

class houzz(scrapy.Spider):
	name = 'houzz'
	domain = 'https://www.houzz.com.au'
	history = []

	def __init__(self):
		pass
	
	def start_requests(self):
		yield scrapy.Request('https://www.houzz.com.au/photos', callback=self.parse_rooms)

	def parse_rooms(self, response):
		count = int(response.xpath('//h1[@class="header-1"]//text()').extract_first().split(' ')[0].replace(',',''))
		if count < 4992 :
			product_list = response.xpath('//div[@class="hz-space-card hz-space-card-xl hz-track-me"]')
			for product in product_list:
				item = ChainItem()
				url = product.xpath('.//a[@class="hz-space-card__image-link-container"]/@href').extract_first()
				item['title'] = product.xpath('.//a[@class="hz-space-card__photo-title header-3 text-unbold"]/text()').extract_first()
				item['save'] = ''.join(product.xpath('.//div[@class="hz-br-spacecard__save-and-question--photo"]//text()').extract()).split('|')[0]
				item['desc'] = product.xpath('.//div[@class="hz-space-card-xl__photo-description"]//text()').extract_first()
				item['long_desc'] = ''
				if product.xpath('.//div[@class="hz-photo-details__auto-description text-s"]//text()').extract_first():
					item['long_desc'] += product.xpath('.//div[@class="hz-photo-details__auto-description text-s"]//text()').extract_first()
				if product.xpath('.//div[@class="hz-photo-details__stats text-s"]//text()').extract_first() : 
					item['long_desc'] += ', ' + product.xpath('.//div[@class="hz-photo-details__stats text-s"]//text()').extract_first()
				item['image'] = product.xpath('.//source/@srcset').extract_first()
				header = {
					"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
					"accept-encoding":"gzip, deflate, br",
					"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
				}
				yield scrapy.Request(url=url, callback=self.parse_detail, headers=header, method="get", meta={'item' : item})
			
			next_bt = response.xpath('//a[@class="hz-pagination-link hz-pagination-link--next"]/@href').extract_first()
			if next_bt:
				next_bt = self.domain + next_bt
				yield scrapy.Request(url=next_bt, callback=self.parse_page)
		else:
			room_list = response.xpath('//div[@class="hz-br-filter-group__body hz-filter-body hz-br-filter-group-room"]//a[@class=" hz-link  clearfix "]/@href').extract()
			for room in room_list:
				yield scrapy.Request(url=room , callback=self.parse_style)

	def parse_style(self, response):
		try:
			count = int(response.xpath('//h1[@class="header-1"]//text()').extract_first().split(' ')[0].replace(',',''))
			if count < 4992 :
				product_list = response.xpath('//div[@class="hz-space-card hz-space-card-xl hz-track-me"]')
				for product in product_list:
					item = ChainItem()
					url = product.xpath('.//a[@class="hz-space-card__image-link-container"]/@href').extract_first()
					item['title'] = product.xpath('.//a[@class="hz-space-card__photo-title header-3 text-unbold"]/text()').extract_first()
					item['save'] = ''.join(product.xpath('.//div[@class="hz-br-spacecard__save-and-question--photo"]//text()').extract()).split('|')[0]
					item['desc'] = product.xpath('.//div[@class="hz-space-card-xl__photo-description"]//text()').extract_first()
					item['long_desc'] = ''
					if product.xpath('.//div[@class="hz-photo-details__auto-description text-s"]//text()').extract_first():
						item['long_desc'] += product.xpath('.//div[@class="hz-photo-details__auto-description text-s"]//text()').extract_first()
					if product.xpath('.//div[@class="hz-photo-details__stats text-s"]//text()').extract_first() : 
						item['long_desc'] += ', ' + product.xpath('.//div[@class="hz-photo-details__stats text-s"]//text()').extract_first()
					item['image'] = product.xpath('.//source/@srcset').extract_first()
					header = {
						"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
						"accept-encoding":"gzip, deflate, br",
						"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
					}
					yield scrapy.Request(url=url, callback=self.parse_detail, headers=header, method="get", meta={'item' : item})
				
				next_bt = response.xpath('//a[@class="hz-pagination-link hz-pagination-link--next"]/@href').extract_first()
				if next_bt:
					next_bt = self.domain + next_bt
					yield scrapy.Request(url=next_bt, callback=self.parse_page)
			else:
				style_list = response.xpath('//div[@class="hz-br-filter-group__body hz-filter-body hz-br-filter-group-style"]//a[@class=" hz-link  clearfix "]/@href').extract()
				for style in style_list:
					yield scrapy.Request(url=style, callback=self.parse_budget)
		except:
			pass
		

	def parse_budget(self, response):
		try:
			count = int(response.xpath('//h1[@class="header-1"]//text()').extract_first().split(' ')[0].replace(',',''))
			if count < 4992 :
				product_list = response.xpath('//div[@class="hz-space-card hz-space-card-xl hz-track-me"]')
				for product in product_list:
					item = ChainItem()
					url = product.xpath('.//a[@class="hz-space-card__image-link-container"]/@href').extract_first()
					item['title'] = product.xpath('.//a[@class="hz-space-card__photo-title header-3 text-unbold"]/text()').extract_first()
					item['save'] = ''.join(product.xpath('.//div[@class="hz-br-spacecard__save-and-question--photo"]//text()').extract()).split('|')[0]
					item['desc'] = product.xpath('.//div[@class="hz-space-card-xl__photo-description"]//text()').extract_first()
					item['long_desc'] = ''
					if product.xpath('.//div[@class="hz-photo-details__auto-description text-s"]//text()').extract_first():
						item['long_desc'] += product.xpath('.//div[@class="hz-photo-details__auto-description text-s"]//text()').extract_first()
					if product.xpath('.//div[@class="hz-photo-details__stats text-s"]//text()').extract_first() : 
						item['long_desc'] += ', ' + product.xpath('.//div[@class="hz-photo-details__stats text-s"]//text()').extract_first()
					item['image'] = product.xpath('.//source/@srcset').extract_first()
					header = {
						"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
						"accept-encoding":"gzip, deflate, br",
						"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
					}
					yield scrapy.Request(url=url, callback=self.parse_detail, headers=header, method="get", meta={'item' : item})
				
				next_bt = response.xpath('//a[@class="hz-pagination-link hz-pagination-link--next"]/@href').extract_first()
				if next_bt:
					next_bt = self.domain + next_bt
					yield scrapy.Request(url=next_bt, callback=self.parse_page)
			else:
				budget_list = response.xpath('//div[@class="hz-br-filter-group__body hz-filter-body hz-br-filter-group-budget"]//a[@class=" hz-link  clearfix "]/@href').extract()
				for budget in budget_list:
					yield scrapy.Request(url=budget, callback=self.parse_size)
		except:
			pass

	def parse_size(self, response):
		try:
			count = int(response.xpath('//h1[@class="header-1"]//text()').extract_first().split(' ')[0].replace(',',''))
			if count < 4992 :
				product_list = response.xpath('//div[@class="hz-space-card hz-space-card-xl hz-track-me"]')
				for product in product_list:
					item = ChainItem()
					url = product.xpath('.//a[@class="hz-space-card__image-link-container"]/@href').extract_first()
					item['title'] = product.xpath('.//a[@class="hz-space-card__photo-title header-3 text-unbold"]/text()').extract_first()
					item['save'] = ''.join(product.xpath('.//div[@class="hz-br-spacecard__save-and-question--photo"]//text()').extract()).split('|')[0]
					item['desc'] = product.xpath('.//div[@class="hz-space-card-xl__photo-description"]//text()').extract_first()
					item['long_desc'] = ''
					if product.xpath('.//div[@class="hz-photo-details__auto-description text-s"]//text()').extract_first():
						item['long_desc'] += product.xpath('.//div[@class="hz-photo-details__auto-description text-s"]//text()').extract_first()
					if product.xpath('.//div[@class="hz-photo-details__stats text-s"]//text()').extract_first() : 
						item['long_desc'] += ', ' + product.xpath('.//div[@class="hz-photo-details__stats text-s"]//text()').extract_first()
					item['image'] = product.xpath('.//source/@srcset').extract_first()
					header = {
						"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
						"accept-encoding":"gzip, deflate, br",
						"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
					}
					yield scrapy.Request(url=url, callback=self.parse_detail, headers=header, method="get", meta={'item' : item})
				
				next_bt = response.xpath('//a[@class="hz-pagination-link hz-pagination-link--next"]/@href').extract_first()
				if next_bt:
					next_bt = self.domain + next_bt
					yield scrapy.Request(url=next_bt, callback=self.parse_page)
			else:
				size_list = response.xpath('//div[@class="hz-br-filter-group__body hz-filter-body hz-br-filter-group-size"]//a[@class=" hz-link  clearfix "]/@href').extract()
				for size in size_list:
					yield scrapy.Request(url=size, callback=self.parse_page)
		except:
			pass

	def parse_page(self, response):
		product_list = response.xpath('//div[@class="hz-space-card hz-space-card-xl hz-track-me"]')
		for product in product_list:
			item = ChainItem()
			url = product.xpath('.//a[@class="hz-space-card__image-link-container"]/@href').extract_first()
			item['title'] = product.xpath('.//a[@class="hz-space-card__photo-title header-3 text-unbold"]/text()').extract_first()
			item['save'] = ''.join(product.xpath('.//div[@class="hz-br-spacecard__save-and-question--photo"]//text()').extract()).split('|')[0]
			item['desc'] = product.xpath('.//div[@class="hz-space-card-xl__photo-description"]//text()').extract_first()
			item['long_desc'] = ''
			if product.xpath('.//div[@class="hz-photo-details__auto-description text-s"]//text()').extract_first():
				item['long_desc'] += product.xpath('.//div[@class="hz-photo-details__auto-description text-s"]//text()').extract_first()
			if product.xpath('.//div[@class="hz-photo-details__stats text-s"]//text()').extract_first() : 
				item['long_desc'] += ', ' + product.xpath('.//div[@class="hz-photo-details__stats text-s"]//text()').extract_first()
			item['image'] = product.xpath('.//source/@srcset').extract_first()
			header = {
				"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
				"accept-encoding":"gzip, deflate, br",
				"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
			}
			yield scrapy.Request(url=url, callback=self.parse_detail, headers=header, method="get", meta={'item' : item})
		
		next_bt = response.xpath('//a[@class="hz-pagination-link hz-pagination-link--next"]/@href').extract_first()
		if next_bt:
			next_bt = self.domain + next_bt
			yield scrapy.Request(url=next_bt, callback=self.parse_page)

	def parse_detail(self, response):
		item = response.meta['item']
		item['title'] = self.validate(item['title'])
		item['save'] = self.validate(item['save'])
		item['desc'] = self.validate(item['desc'])
		item['long_desc'] = self.validate(item['long_desc'])
		item['image'] = response.xpath('//div[@class="viewSpaceImage"]//img/@src').extract_first()
		if item['title']+item['image'] not in self.history:
			self.history.append(item['title']+item['image'])
			yield item
		# if response.xpath('//div[@class="viewSpaceImage"]//img/@src').extract_first():
		# 	yield scrapy.Request(url=response.xpath('//div[@class="viewSpaceImage"]//img/@src').extract_first(), callback=self.parse_image)
	
	def parse_image(self, response):
		with open('houzz/' + '-'.join(response.url.split('/')[-2:]), 'wb') as f:
			f.write(response.body)

	def validate(self, item):
		try:
			return item.strip().replace('\n', '').replace('\t','').replace('\r', '').replace(';','')
		except:
			pass

	def eliminate_space(self, items):
	    tmp = []
	    for item in items:
	        if self.validate(item) != '':
	            tmp.append(self.validate(item))
	    return tmp

	def str_concat(self, items, unit):
	    tmp = ''
	    for item in items[:-1]:
	        if self.validate(item) != '':
	            tmp += self.validate(item) + unit
	    tmp += self.validate(items[-1])
	    return tmp

