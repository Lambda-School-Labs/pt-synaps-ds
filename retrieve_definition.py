#!/usr/bin/python3

"""
    Pull first 300 characters from Wikipedia article for a given term
"""

import requests
import inflect

# Start engine for text_wrangle() singularization
p = inflect.engine()


def retrieve_definition(term, term_wrangled=False):

    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "exchars": "300",
        "titles": term,
        "format": "json",
        "explaintext": 1,
        "exlimit": 1
    }

    # parameters set to query for an extract of 300 characters for the given term, in JSON format. Explaintext strips
    # out Wikipedia's special formatting. Exlimit says to only return 1 extract.

    print("Searching API for: ", term)
    response = S.get(url=URL, params=params)
    data = response.json()
    pageid = list(data['query']['pages'].keys())[0]
    try:
        print("Pulling extract")
        extract = data['query']['pages'][pageid]['extract']
        print(extract)
        # this selects the extract from within the JSON object returned by the API call. Two steps are necessary
        # because one of the dictionary keys is the page ID for that term.

        # if the length of extract is 3, that indicates extract is '...',
        # which is what the API usually returns if it doesn't find a page
        if len(extract) > 3:
            return extract

        elif (len(extract) == 3 and term_wrangled == False):
            wrangled_term = text_wrangle(term)
            print("Wrangled_term: ", wrangled_term)
            wrangled_extract = retrieve_definition(wrangled_term,
                                                term_wrangled=1)
            print(len(wrangled_extract))
            if len(wrangled_extract) > 3:
                return wrangled_extract

            else:
                return open_search(term)

        else:
            return open_search(term)
            
    except KeyError:
        # sometimes instead of an empty string as an extract the API call returns a "missing" key in JSON, this accounts
        # for that
        return open_search(term)

def open_search(term):
    """
    function to use opensearch on Wikipedia API and return most likely related articles for a given term. opensearch
    is a Wikimedia API feature which returns similarly-titled articles within the wiki.
    """
    
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "opensearch",
        "search": term,
        "redirects": "resolve",
        "format": "json"
    }

    # Parameters set tells API to use opensearch on the given term and return the results as a JSON object.
    # Resolve means to return redirects as the page they point to.


    R = S.get(url=URL, params=params)
    DATA = R.json()
    suggests = DATA[1]
    try:
        return f"Did you mean {suggests[0]}, {suggests[1]}, {suggests[2]}?"
    
    except IndexError:
        # This covers cases where input doesn't have a close Wiki entry
        return "We can't find anything close to that :("


def text_wrangle(term):
    """
    Check text for various edge cases and remove
    """
    if term.isupper():
        # Makes term lowercase
        term = term.lower()
        print("Lowercase search: ", term)

    if term[0:4] == 'the ':
        # Strips 'the' and 'The' from term
        term = term[4:]
        print("Search without 'the': ", term)

    if term[0:2] == 'a ':
        term = term[2:]
        print("Search without 'a': ", term)
    
    if p.singular_noun(term):
        term = p.singular_noun(term)
        print("Search as singular: ", term)

    return term
