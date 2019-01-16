import urllib2, json, time, os, math

if os.path.isfile('KeyForgeDecks.json'):
	with open('KeyForgeDecks.json') as f:
	    decks = json.load(f)
else:
	decks = {}

if os.path.isfile('KeyForgeCards.json'):
	with open('KeyForgeCards.json') as f:
	    cards = json.load(f)
else:
	cards = {}		

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

iPageSize = 25

dGetVars = {
	'page': int(math.floor(len(decks) / iPageSize)) + 1,
	'page_size': iPageSize,
	'ordering': 'date',
	'links': 'cards',
}

iTotal = 0
iSoFar = len(decks)

iStartTime = time.time()

while iTotal > len(decks) or iTotal == 0:
	sGetVars = ''
	s = '?'
	for key in dGetVars:
		sGetVars += s + key + '=' + str(dGetVars[key])
		s = '&'

	url = "https://www.keyforgegame.com/api/decks/" + sGetVars

	response = opener.open(url)
	data = json.loads(response.read())

	iTotal = data['count']

	for aNewDeck in data['data']:
		decks[aNewDeck['id']] = {
			'name': aNewDeck['name'],
			'cards': aNewDeck['_links']['cards']
		};
		for card in aNewDeck['_links']['cards']:
			if card not in cards:
				for dCardData in data['_linked']['cards']:
					if dCardData['id'] == card:
						cards[card] = dCardData

				with open('KeyForgeCards.json', 'w') as f:
					json.dump(cards, f)

	with open('KeyForgeDecks.json', 'w') as f:
		json.dump(decks, f)
			
		
	print str(len(decks)) + '/' + str(iTotal) + ' decks (' + str(len(decks)/float(iTotal)*100) + '%)'

	dGetVars['page'] = int(math.floor(len(decks) / iPageSize)) + 1

	print str(((time.time() - iStartTime) / (len(decks) - iSoFar)) * (iTotal - len(decks)) / 60 / 60) + ' hours (decimal, approx)'