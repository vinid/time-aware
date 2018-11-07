import wikipedia
import spotlight
from nltk.corpus import stopwords
import argparse
import logging

def get_page(year):
    replacing_this = [",", ":"]
    removal = "== Births =="
    events = "== Events =="

    remove_months = ["January", "February", "March", "April", "May", "June",
                     "July", "August", "September", "October", "November", "December"]

    p = wikipedia.page(str(year)) #get page of year

    rest = p.content.split(removal, 1)[0].replace("\n", " ")

    rest = rest.split(events, 1)[1] # getting only text between events and births

    for k in remove_months:
        rest = rest.replace(k, " ") # remove months
    for k in replacing_this:
        rest = rest.replace(k, " ") # remove chars

    return rest

def clean_page(page):
    stops = stopwords.words('english')
    filtered_words = [word for word in page.split() if word not in stops]
    page = " ".join(filtered_words)
    return page


def annotate(string):
    text_saved_annotated = []
    annotations = []
    try:
        annotations = spotlight.annotate("http://model.dbpedia-spotlight.org/en/annotate",
        string,
        confidence = 0.5, support = 0)
    except:
        pass

    for k in annotations:
        text_saved_annotated.append(k["URI"].replace("http://dbpedia.org/resource/", ""))
    final_sentence = " ".join(text_saved_annotated).encode("utf-8")
    return final_sentence



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-starting_year', '--sy',help="", type=int)
    parser.add_argument('-ending_year', '--ey',help="", type=int)
    parser.add_argument('-annotate', '--an',help="Use Spotlight to annotate or just get words", type=int)
    args = parser.parse_args()

    years = range(args.starting_year, args.ending_year)

    pages = map(get_page, years)
    logging.info("Pages Extracted")
    zipped_years_and_pages = zip(years, pages)

    logging.info("Now Annotationg")


    for year, page in zipped_years_and_pages:
        with open("/years_annotated/" + str(year), "w") as ff:
            if args.annotate:
                ff.write(annotate(page.encode("utf-8")) + "\n")
            else:
                ff.write(page.encode("utf-8")+ "\n")

