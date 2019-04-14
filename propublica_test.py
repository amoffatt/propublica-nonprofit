"""
utility to find EIN numbers based on other org info (name, address, state, etc.)
needed to enrich school profiles
search parameters at propublica api docs:  https://projects.propublica.org/nonprofits/api
c_code[id] =3 for 501(c)(3)
"""

from nonprofit import Nonprofit


npft = Nonprofit()

def filter_exact_match(search_string, orgs):
    """
    filters list of org dicts by name, based on exact match of propublica query search string
    :param orgs: nonprofit search results (list of dicts)
    :return: result object, list of single dict or null
    """

    # imperfect easy solution -- if
    # perfect hard solution
    # regex example, searching for words that match multiple words, with spaces
    # need to extend to take any arbitrary input of words
    # >> > import re
    # >> > string = 'NAME: "test1",  DESCR: "AAA 1111S ABC 48 BB (4 BBBB) TEST1
    # >> > sol = re.findall('\w{3}\s\w{5}', string)
    # >> > sol

    return True

# query by multiple parameters (q, state, c_code, state)
search_string = "ODYSSEY SCHOOL"
orgs = npft.search.get(q=f"{search_string}", c_code=3, state="CA", )

print(type(orgs))
for i in range(len(orgs)):
    print(orgs[i])


# use fetch to access endpoints directly
# orgs = npft.fetch('search.json?q=delta')
# orgs['total_results']
