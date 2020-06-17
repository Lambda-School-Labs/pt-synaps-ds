#!/usr/bin/python3

"""
    Pull first 300 characters from Wikipedia article for a given term
"""

import requests
import inflect

# Start engine for text_wrangle() singularization
p = inflect.engine()


def retrieve_definition(term):

    S = requests.Session()

<<<<<<< HEAD
    URL = "https://en.wikipedia.org/w/api.php"
    term = text_wrangle(term)
=======
    # this is the base API URL for Wikipedia
    URL = "https://en.wikipedia.org/w/api.php"

>>>>>>> origin/master
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
    # out Wikipedia's special formatting. Exlimit says to only return 1
    # extract.

    print("Searching API for: ", term)
    response = S.get(url=URL, params=params)
    data = response.json()
    pageid = list(data['query']['pages'].keys())[0]
    try:
        extract = data['query']['pages'][pageid]['extract']
        # this selects the extract from within the JSON object returned by the API call. Two steps are necessary
        # because one of the dictionary keys is the page ID for that term.

        if len(extract) == 3:
            return open_search(term)

        else:
            return extract
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

<<<<<<< HEAD

    R = S.get(url=URL, params=params)
=======
    R = S.get(url=URL, params=PARAMS)
>>>>>>> origin/master
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
<<<<<<< HEAD
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
=======
        wrangled_search = retrieve_definition(term.lower())
    elif (term[0:4] == 'the ') | (term[0:4] == 'The '):

        wrangled_search = retrieve_definition(term[4:])
        # sends term back through function minus 'the'
    elif term[-1:] == 's':
        wrangled_search = retrieve_definition(term[:-1])
        # sends terms back through function without final 's'
    elif term[-1:] == 'e':
        # this accounts for cases of "es" plural, the previous cycle would have
        # removed the 's'
        wrangled_search = retrieve_definition(term[:-1])
    if len(wrangled_search) > 3:
        return wrangled_search

    else:
        return open_search(term)
        # all of the test cases have failed, function will return suggestions
        # instead
>>>>>>> origin/master
