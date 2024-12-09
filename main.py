# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import sys
import traceback
import urllib.parse



ME = 'Firaja'

BASE_URL = 'https://acquageraci.forumfree.it'

def get_parser(url, base=''):
	headers = {'User-Agent': 'Mozilla/5.0'}
	html_text = requests.get(f'{base}{url}', headers=headers)
	return BeautifulSoup(html_text.text, 'html.parser')


def search(dictionary, search_string):
	for key,val in dictionary.items():
		if ME in val:
			return (key, val)


def filter_items(selector):
	result = []
	for element in selector:
		if ME in element.text:
			result.append(element)
	result = result[-1].contents

	for i in  range(len(result)):
		result[i] = result[i].text.replace('\n', '').replace('\t', '')

	result = list(filter(lambda a: a != '', result))

	return result

def encode(body):
	
	table = {}
	
	for line in body:
		splitted_line = line.split(': ')
		usernames = splitted_line[0]
		score = int(splitted_line[1])
		table[score] = usernames
	
	return table

def decode(table):
	body = ''
	sorted_keys = sorted(table.keys(), reverse=True)
	for key in sorted_keys:
		body += f'{table[key]}: {key}\n'
	return body[:-1]


def send(body):
	cookies = {
		'_ga': 'GA1.2.1374593745.1730925141',
		'cpop': '1',
		'sb_0': 'e30=',
		'login-from': 'https%253A%252F%252Firc.forumfree.it%252Fchat%252FScripts%252FChatEngine.js',
		'member_id': '7168097',
		'pass_hash': '1d3f7c305c93375ee4f792e022fb2a5de35419ed9c8014fc2190905833736d90',
		'__samesite_migration': 'migrated',
		'sb_7168097': 'e30=',
		'cat': '191706',
		'session_id': '0ba56d35f73ace9c4102d0915990ab69',
		'unread': '0%2C0%2C0',
		'resolution': '1792x1120',
		'auth_session': 'nojjtknftkpodi4ys2ogq2tfm5vgo',
		'pop1': '8',
		'MgidStorage': '%7B%220%22%3A%7B%22svspr%22%3A%22%22%2C%22svsds%22%3A4%7D%2C%22C719965%22%3A%7B%22page%22%3A1%2C%22time%22%3A%221733732465537%22%7D%7D',
		'notification_unread': '0%2C0',
	}

	headers = {
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,it;q=0.7',
		'cache-control': 'no-cache',
		'content-type': 'application/x-www-form-urlencoded',
		'cookie': '_ga=GA1.2.1374593745.1730925141; cpop=1; sb_0=e30=; login-from=https%253A%252F%252Firc.forumfree.it%252Fchat%252FScripts%252FChatEngine.js; member_id=7168097; pass_hash=1d3f7c305c93375ee4f792e022fb2a5de35419ed9c8014fc2190905833736d90; __samesite_migration=migrated; sb_7168097=e30=; cat=191706; session_id=0ba56d35f73ace9c4102d0915990ab69; unread=0%2C0%2C0; resolution=1792x1120; auth_session=nojjtknftkpodi4ys2ogq2tfm5vgo; pop1=8; MgidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22%22%2C%22svsds%22%3A4%7D%2C%22C719965%22%3A%7B%22page%22%3A1%2C%22time%22%3A%221733732465537%22%7D%7D; notification_unread=0%2C0',
		'origin': 'https://acquageraci.forumfree.it',
		'pragma': 'no-cache',
		'priority': 'u=0, i',
		'referer': 'https://acquageraci.forumfree.it/?t=36639860&st=114645',
		'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"macOS"',
		'sec-ch-ua-platform-version': '"14.7.1"',
		'sec-fetch-dest': 'document',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-user': '?1',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
	}

	data = 'st=0&act=Post&s=0ba56d35f73ace9c4102d0915990ab69&f=6409732&CODE=03&t=36639860&TopicTime=&Post='
	data += urllib.parse.quote_plus(body.replace('\n', '<br>'), encoding='cp1252')

	print(data)

	# return requests.post('https://acquageraci.forumfree.it/', cookies=cookies, headers=headers, data=data)



def main():
	url = sys.argv[1]

	parser = get_parser(url)
	links = [l for l in parser.findAll("a") if ('36639860' in l.get('href') and '#newpost' in l.get('href'))]

	last_post_url = links[0].get('href')

	print(f'Last post is at {last_post_url}')


	parser = get_parser(last_post_url, base=BASE_URL)


	body = filter_items(parser.select('table.color td'))


	table = encode(body)

	print(table)

	actual_score, actual_usernames = search(table, ME)
	print((actual_score, actual_usernames))

	alone = ', ' not in actual_usernames

	new_score = actual_score + 1
	new_actual_usernames = ', '.join(list(filter(lambda a: a != ME, actual_usernames.split(', '))))

	print(f'new_actual_usernames: {new_actual_usernames}')

	if alone:
		del table[actual_score]
	else:
		table[actual_score] = new_actual_usernames

	if new_score in table:
		table[new_score] = f'{table[new_score]}, {ME}'
	else:
		table[new_score] = ME

	new_body = decode(table)

	print(new_body)

	send(new_body)




if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(traceback.format_exc())
	else:
		pass
	finally:
		exit(0)
	
