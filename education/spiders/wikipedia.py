# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from education.items import EducationItem


class WikipediaSpider(scrapy.Spider):
	name = "wikipedia"
	allowed_domains = ["wikipedia.org"]
	start_urls = [
				  "https://en.wikipedia.org/wiki/Portal:Contents/Geography_and_places",
				  "https://en.wikipedia.org/wiki/Portal:Contents/Reference",
				  "https://en.wikipedia.org/wiki/Portal:Contents/Culture_and_the_arts",
				  "https://en.wikipedia.org/wiki/Portal:Contents/Health_and_fitness",
				  "https://en.wikipedia.org/wiki/Portal:Contents/History_and_events",
				  "https://en.wikipedia.org/wiki/Portal:Contents/Mathematics_and_logic",
				  "https://en.wikipedia.org/wiki/Portal:Contents/Natural_and_physical_sciences",
				  "https://en.wikipedia.org/wiki/Portal:Contents/People_and_self",
				  "https://en.wikipedia.org/wiki/Portal:Contents/Philosophy_and_thinking",
				  "https://en.wikipedia.org/wiki/Portal:Contents/Religion_and_belief_systems",
				  "https://en.wikipedia.org/wiki/Portal:Contents/Society_and_social_sciences",
				  "https://en.wikipedia.org/wiki/Portal:Contents/Technology_and_applied_sciences",
				  ]

	def parse(self,response):
		main_categories = response.xpath('//div[@class="hlist"]/ul/li/a/@href').extract()
		for cate in main_categories:
			link = "https://en.wikipedia.org" + cate if cate else None
			# print "==========================",link
			if link:
				yield Request(url=link, callback=self.categoryPages)

	def categoryPages(self,response):
		# print "===============",response.url
		catePage = response.xpath('//div[@class="mw-category"]/div/ul/li/a/@href').extract_first()
		catePageLink = "https://en.wikipedia.org" + catePage if catePage else None
		# print "========================",catePageLink
		if catePageLink:
			yield Request(url=catePageLink, callback=self.details)

	def details(self, response):
		item = EducationItem()
		# print "!!!!!!!!!!!!!!!!!!!!!!!!",response.url
		l = ItemLoader(item=EducationItem(), response=response)
		l.add_xpath('title', '//h1[@id="firstHeading"]')
		title = l.get_output_value('title')
		# print "++++++++++++++++++++++++++++++",title

		l.add_xpath('details', '//div[@class="mw-parser-output"]/p')
		details = l.get_output_value('details')
		# print "==================",details

		return l.load_item()
		print "============================",item



