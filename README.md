# Ebay Scraper

In [this project](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03), I wrote a python script that takes information from eBay search results and returns them into either a JSON file or CSV file, based on the user's input. The information that is returned includes the result's name, price, status, shipping cost, whether the product has free returns, and the number of items sold.

## How to run the code

To run the code, enter the following (replace <code>oneword</code> or <code>two words</code> with whatever you want). If <code>your_search</code>is more than one word, wrap it in quotation marks. See the following examples.

```
$ python3 ebay-dl.py oneword
$ python3 ebay-dl.py 'two words'
```

## Returning a CSV file

To get a CSV file instead of a JSON file, add a <code>--csv=True</code> to the end of your command. 

```
$ python3 ebay-dl.py 'one word' --csv=True
$ python3 ebay-dl.py 'two words' --csv=True
```

The code by default returns the first ten pages of results. However, you can manually set the number of pages returned by appending <code>--num_pages</code> flag. 

```
$ python3 ebay-dl.py 'two words' --num_pages=5
```
