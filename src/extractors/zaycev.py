#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup
from . import baseFile

class interface(object):

	def __init__(self):
		self.results = []
		self.name = "zaycev"
		self.needs_transcode = False

	def search(self, text, page=1):
		site = 'http://go.mail.ru/zaycev?q=%s&page=%s' % (text, page)
		r = requests.get(site)
		soup = BeautifulSoup(r.text, 'html.parser')
		D = r'длительность.(\d+\:\d+\:\d+)'
		R = r'размер.((\d+|\d+.\d+) \w+)'
		B = r'битрейт.(\d+ \w+)'
		self.dh = [[x.get_text(), x.get('href')]for x in soup.find_all('a', {'class': "light-link"}) if x.get_text() != "Читать далее"]
		self.hd = [{'duration': re.search(D, str(x)).group()[13:], 'size': re.search(R, str(x)).group()[7:], 'bitrate': re.search(B, str(x)).group()[8:]} for x in soup.find_all('div', {'class': "result__snp"})]
		self.results = []
		for i in range(len(self.hd)):
			s = baseFile.song(self)
			s.title = self.dh[i][0]
			s.url = self.dh[i][1]
			s.duration = self.hd[i]["duration"]
			s.size = self.hd[i]["size"]
			s.bitrate = self.hd[i]["bitrate"]
			self.results.append(s)

	def get_download_url(self, url):
		soups = BeautifulSoup(requests.get(url).text, 'html.parser')
		data = json.loads(requests.get('http://zaycev.net' + soups.find('div', {'class':"musicset-track"}).get('data-url')).text)
		return data["url"]