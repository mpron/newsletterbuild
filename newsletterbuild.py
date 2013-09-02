import csv
from sys import argv

script, filename = argv

zones = ["Javalobby", "agile_stream", "bigdata_stream", "cloud_stream", 
"devops_stream", "enterprise-integration_stream", "high-perf_stream", 
"html5_stream", "mobile_stream", "nosql_stream"]

def buildDictionary(filename):
    result = {}

    for zone in zones:
        with open(filename, 'rU') as f:
            reader = csv.reader(f)
            flag = 0
            articles = []
            for row in reader:
                if flag < 3:
                    if row[0] == zone:
                        article = {"title":row[3],"url":row[2],"author":row[4],"description":row[5]}
                        articles.append(article)
                        flag += 1
                        print flag
                else:
                    result[zone] = articles
    return result

allTopArticles = buildDictionary(filename)

finalDocument = open("template_gen.txt", "w")

#finalDocument.write(section1)

#Need to do ordered list somehow to put Javalobby and others in any order I want,
#Need to proper titles that connect to the _stream keys

def buildTemplate(zone):
    section = """
    
    %s[zone]

    %s[title(1st place views)] - %s[author(1st place views)] 
    %s[description(1st place views)] 
    %s[url(1st place views)] 

    %s[title(2nd place views)] - %s[author(2nd place views)] 
    %s[url(2nd place views)] 

    %s[title(3rd place views)] - %s[author(3rd place views)] 
    %s[url(3rd place views)] 


    """ % zone, allTopArticles[zone][0]["title"], allTopArticles[zone][0]["author"], 
    allTopArticles[zone][0]["description"], allTopArticles[zone][0]["url"],
    allTopArticles[zone][1]["title"], allTopArticles[zone][1]["author"], allTopArticles[zone][1]["url"],
    allTopArticles[zone][2]["title"], allTopArticles[zone][2]["author"], allTopArticles[zone][2]["url"]
    
    return section

for zone in zones:
    foo = buildTemplate(zone)
    finalDocument.write(foo)


#finalDocument.write(section3)

finalDocument.close()