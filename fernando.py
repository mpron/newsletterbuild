#! /usr/bin/env python

import sys
import csv
import uuid
import pprint
import logging
from argparse import ArgumentParser

class Filter:
    """ Inteface / Abstract Class concept for readability. """

    def apply(self, articles):
        raise NotImplementedError('Exception raised, Filter is supposed to be an interface / abstract class!')

class MyFilter(Filter):
    """ Filters articles by views"""

    def apply(self, articles):
        #sort articles by viewcount
        sorted_articles = sorted(articles,key=lambda article: article['views'], reverse=True)
        #keep first 3 most viewed articles for every category
        #TODO: add filtering for first 3 articles coming from cli or csv
        zones = set([article["zone"] for article in articles])
        result = []
        for zone in zones:
            filtered_sorted_articles = filter(lambda article: article["zone"] == zone, sorted_articles)
            pprint.pprint(filtered_sorted_articles, width=20)
            if len(filtered_sorted_articles) >= 3:
                result.append(filtered_sorted_articles[2])
            else:
                result.append(filtered_sorted_articles[-1])
        print "mierdita"
        pprint.pprint(result, width=20)
        return result

class CategorizationStrategy:
    """ Inteface / Abstract Class concept for readability. """

    def categorize(self, articles):
        raise NotImplementedError('Exception raised, CategorizationStrategy is supposed to be an interface / abstract class!')

class ZoneCategorizationStrategy(CategorizationStrategy):
    """ Categorizes articles by zone"""

    def categorize(self, articles):
        result = {}
        for article in articles:
            if result.get(article["zone"]):
                result.get(article["zone"]).append(article)
            else:
                result[article["zone"]] = [article]
        return result

class AuthorCategorizationStrategy(CategorizationStrategy):
    """ Categorizes articles by author"""

    def categorize(self, articles):
        result = {}
        for article in articles:
            if result.get(article["author"]):
                result.get(article["author"]).append(article)
            else:
                result[article["author"]] = [article]
        return result

def get_default_filter():
    return MyFilter()

def get_default_categorization_strategy():
    return ZoneCategorizationStrategy()

def get_categorization_strategy(categorization_strategy_name):
    return get_default_categorization_strategy()

def get_articles_lists(filename):
    articles = []
    zone_index=0
    url_index=1
    views_index=2
    author_index=3
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            articles.append({"zone":row[zone_index],"url":row[url_index],"views":int(row[views_index]),"author":row[author_index]})
    return articles

def get_newsletter_articles(articles,filter,categorization_strategy):
    """Filter and categorize articles"""
    return categorization_strategy.categorize(filter.apply(articles))

def create_plain_text_newsletter(articles):
    return articles

def create_html_newsletter(articles):
    return articles

def parse_args():
    """cli interface helpers"""

    description = "usage: %prog [options] arg1 arg2"
    parser = ArgumentParser(description=description)
    parser.add_argument("-v","--verbose",help="increase output verbosity",action="store_true")
    parser.add_argument("--articles-file-name",required=True,action="store",dest="articles_file_name",help="read articles from FILENAME")
    #parser.add_argument("--zone-names",nargs='*',action="store",dest="zone_names",help="read zones from ZONES")
    parser.add_argument("--zones-file-name",action="store",dest="zones_file_name",help="read zones from FILENAME")
    parser.add_argument("--output-file-name",default="output_"+str(uuid.uuid4()),action="store",dest="output_file_name",help="output to FILENAME")
    #parser.add_argument("--output-type",choices=["rich-html","plain-html"],default="zones",action="store",dest="categorization_strategy_name",help="categorize by CRITERIA")
    #parser.add_argument("--template-file-name",action="store",dest="template_file_name",help="use FILENAME as template")
    parser.add_argument("--categorization",choices=["zones","author"],default="zones",action="store",dest="categorization_strategy_name",help="categorize by CRITERIA")
    return parser.parse_args()

if __name__ == "__main__":
    """main app loop"""

    args = parse_args()
    
    #configure logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG,format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO,format='%(levelname)s: %(message)s')

    articles = get_articles_lists(args.articles_file_name)
    newsletter_articles = get_newsletter_articles(articles,get_default_filter(),get_categorization_strategy(args.categorization_strategy_name))
    
    #TODO: Add logic to make this thing spit html files (maybe use jinja?)
    #create_html_newsletter(newsletter_articles)
    text_file = open(args.output_file_name, 'w')
    pprint.pprint(newsletter_articles,text_file, width=20)
    text_file.close()
    logging.info( "Saved results to file %s" %args.output_file_name)



