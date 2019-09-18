import wikipedia as wiki


def do_wiki(search_term):

    found = wiki.summary(search_term, sentences=2)

    return found
