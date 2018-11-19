import wikipedia
import spotlight
from nltk.corpus import stopwords
import argparse
import logging
import pathlib


def get_page(year):
    replacing_this = [',', ':']
    removal = '== Births =='
    events = '== Events =='

    remove_months = ['January', 'February', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November', 'December']

    year = (str(year * -1) + '_BC') if year < 0 else ('AD_' + str(year))
    print(year)
    p = wikipedia.page(str(year))  # get page of year

    rest = p.content.split(removal, 1)[0].replace("\n", " ")

    if events in rest:
        rest = rest.split(events, 1)[1]  # getting only text between events and births

    for k in remove_months:
        rest = rest.replace(k, " ")  # remove months
    for k in replacing_this:
        rest = rest.replace(k, " ")  # remove chars

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
                                         string, confidence=0.5, support=0)
    except:
        pass

    for k in annotations:
        text_saved_annotated.append(k["URI"].replace("http://dbpedia.org/resource/", ""))
    final_sentence = " ".join(text_saved_annotated)
    return final_sentence


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--starting_year', '-sy', help="The start of years you want to generate embeddings", type=int,
                        required=True)
    parser.add_argument('--ending_year', '-ey', help="The end of years you want to generate embeddings", type=int,
                        required=True)
    parser.add_argument('--annotate', '-an', help="Use Spotlight to annotate or just get words", type=int)
    args = parser.parse_args()

    years = list(range(args.starting_year, args.ending_year))
    if 0 in years:
        years.remove(0)  # year zero does not exist

    pages = map(get_page, years)
    logging.info("Pages Extracted")
    zipped_years_and_pages = zip(years, pages)

    logging.info("Now Annotation")

    dest = 'years_annotated/'
    pathlib.Path(dest).mkdir(parents=True, exist_ok=True)

    for year, page in zipped_years_and_pages:
        with open(dest + str(year), "w", encoding='utf-8') as ff:
            if args.annotate:
                ff.write(annotate(page.encode("utf-8")))
            else:
                ff.write(page)
            ff.write("\n")
