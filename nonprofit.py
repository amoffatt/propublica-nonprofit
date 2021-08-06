"""
A Python client for the ProPublica Nonprofit Explorer API.

API docs: https://www.propublica.org/datastore/api/nonprofit-explorer-api
"""

import sys
import json
import urllib
import httplib2
from types import SimpleNamespace


def check_ntee(ntee):
    """
        Returns true if ntee is a valid NTEE code; false otherwise.
    """
    ntees = range(1, 11)

    if ntee not in ntees:
        raise TypeError('Invalid ntee code')


def check_c_code(c_code):
    """
        Returns true if c_code is a valid tax code id; false otherwise.
    """
    c_codes = list(range(2, 29))
    c_codes.append(92)

    if c_code not in c_codes:
        raise TypeError('Invalid c_code')


def check_state(state):
    """
        Returns true if state is a valid US state code; false otherwise.
    """
    states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "ZZ"]

    if state not in states:
        raise TypeError('Invalid state code')


class NonprofitError(Exception):
    """ Exception for general Nonprofit client errors """

    def __init__(self, message, resp=None, url=None):
        super(NonprofitError, self).__init__(message)
        self.message = message
        self.resp = resp
        self.url = url


    def _result_to_str(self, result):
        return 
    
    
class NonprofitObject(SimpleNamespace):
    def __init__(self, obj):
        super().__init__(**obj)
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def json_loads(content):
    return json.loads(content, object_hook=NonprofitObject)
    

class Client(object):

    BASE_URI = "https://projects.propublica.org/nonprofits/api/v2/"

    def __init__(self, cache='.cache'):
        self.http = httplib2.Http(cache)


    def fetch(self, path, parse=''):
        """ Make the API request. """
        url = self.BASE_URI + path

        resp, content = self.http.request(url)
        content = json_loads(content)

        # TODO: check for content not found
        if not resp.get('status') == '200':
            raise NonprofitError(content, resp, url)

        if callable(parse):
            content = parse(content)

        return content


class SearchClient(Client):

    def get(self, **kwargs):
        """
            Returns a list of organizations matching the given search terms.
        """

        params = {}
        for key, value in kwargs.items():

            if key == 'state':
                check_state(value)
                key = 'state[id]'

            if key == 'ntee':
                check_ntee(value)
                key = 'ntee[id]'

            if key == 'c_code':
                check_c_code(value)
                key = 'c_code[id]'

            params[key] = value

        params = urllib.parse.urlencode(params)
        path = 'search.json?%s' % (params)
        result = self.fetch(path)
        
        result.all_organizations = lambda max_results=0: self._get_all_orgs(max_results=max_results, **kwargs)
        
        return result
    
    def _get_all_orgs(self, max_results=0, **kwargs):
        """
        Returns a generator of all queried organizations. Will make HTTP requests for subsequent API pages as the
        generator runs, if there are more results than can fit on a single page.
        Raises a NonprofitError if the query has more results than the ProPublica API can return (> 10,000).
        """
        page = 0
        remaining_pages = True
        i = 0
        while remaining_pages:
            result = self.get(page=page, **kwargs)
            
            if page == 0:
                # only evaluate results overflow on the first page.
                # If more results than API can return, and user defined max_results does not explicitly request fewer than the API's max, then raise an error
                api_max_results = result.num_pages * result.per_page
                
                if result.total_results > api_max_results and (max_results == 0 or max_results > api_max_results):
                    raise NonprofitError(f"Search has more results than ProPublica API can return ({result.total_results}). Try setting the max_results argument to a number <= {api_max_results}.")

            for o in result.organizations:
                yield o
                i += 1
                
                if max_results > 0 and i >= max_results:
                    return
            
            remaining_pages = page < result.num_pages
            
                
            page += 1
        


class OrgsClient(Client):

    def get(self, ein):
        """ Returns an organization object for the given employer
            identification number (ein).
        """
        path = 'organizations/{0}.json'.format(ein)
        return self.fetch(path)


class Nonprofit(Client):
    """
        The public interface for the Nonprofit API client.
    """

    def __init__(self, cache='.cache'):
        super(Nonprofit, self).__init__(cache)
        self.search = SearchClient(cache)
        self.orgs = OrgsClient(cache)
