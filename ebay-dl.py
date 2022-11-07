import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv

def parse_prices(text):
    if 'see current price' in text.lower():
        return None
    else:
        price = ''
        for char in text:
            if char in '0123456789':
                price += char
            if char not in '$.0123456789':
                break
        return int(price)

def parse_shipping(text):
    if 'free ' in text.lower():
        return 0
    else:
        shipping_price = ''
        for char in text:
            if char in '0123456789':
                shipping_price += char
            if char == ' ':
                break
    return int(shipping_price)


def parse_itemssold(text):
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return None

    # Get command line arguments
parser = argparse.ArgumentParser(description='Download information from eBay and convert to JSON.')
parser.add_argument('search_term')
parser.add_argument('--num_pages', default = 10)
parser.add_argument('--csv', nargs='?', const=True)
args = parser.parse_args()
print('args.search_term=', args.search_term)

# List of all itmes found in all eBay webpages
items = []

# Loop over the eBay webpages
for page_number in range(1, int(args.num_pages)+1):

    # Build the URL
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + args.search_term + '&_sacat=0&_pgn=' +str(page_number) + '&rt=nc'
    print('url=', url)

    # Download the HTML
    r = requests.get(url)
    status = r.status_code
    print('status=', status)
    html = r.text

    # Process the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Loop over the items in the page
    tags_items = soup.select('.s-item')
    for tag_item in tags_items:

        # Extract the name
        name = None
        tags_name = tag_item.select('.s-item__title')
        for tag in tags_name:
            name = tag.text

        # Extract the price
        price = None
        tags_price = tag_item.select('.s-item__price')
        for tag in tags_price:
            price = parse_prices(tag.text)

        # Extract the status
        status = None
        tags_status = tag_item.select('.SECONDARY_INFO')
        for tag in tags_status:
            status = tag.text

        # Extract the shipping
        shipping = None
        tags_shipping = tag_item.select('.s-item__shipping,.s-item__freeXDays')
        for tag in tags_shipping:
            shipping = parse_shipping(tag.text)

        # Extract the freereturns
        freereturns = False
        tags_freereturns = tag_item.select('.s-item__free-returns')
        for tag in tags_freereturns:
            freereturns = True

        # Extract the items_sold
        items_sold = None
        tags_itemssold = tag_item.select('.s-item__hotness')
        for tag in tags_itemssold:
            items_sold = parse_itemssold(tag.text)

        item = {
            'name': name,
            'price': price,
            'status': status,
            'shipping': shipping,
            'free_returns': freereturns,
            'items_sold': items_sold,
        }
        items.append(item)

    print('len(tags_items)=', len(tags_items))
    print('len(items)=', len(items))

if args.csv:
# Write the CSV to a file
    filename = args.search_term + '.csv'
    with open(filename, 'w', encoding='utf-8') as f:
        file = csv.DictWriter(f, fieldnames=list(items[0].keys()))
        file.writeheader()
        file.writerows(items)
else:
# Write the JSON to a file
    filename = args.search_term + '.json'
    with open(filename, 'w', encoding='ascii') as f:
        f.write(json.dumps(items))
