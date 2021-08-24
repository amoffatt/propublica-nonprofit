# Propublica Nonprofit Explorer Client
**[forked from: https://github.com/robrem/propublica-nonprofit][https://github.com/robrem/propublica-nonprofit]**


Python client for the ProPublica [NonProfit Explorer API](https://www.propublica.org/datastore/api/nonprofit-explorer-api "ProPublica Nonprofit Explorer API docs").

Query data on over 1.6 million nonprofit organizations. No API key is required, but please refer to ProPublica's terms of use.

Changed to work with Python 3+ syntax only.

## Usage
```
>>> from nonprofit import Nonprofit
>>> np = Nonprofit()

# get organization by employer identification number (EIN)
>>> org = np.orgs.get('931309725')
>>> org.organization.name
'SCIENCEWORKS HANDS-ON MUSEUM'

# get data for the most recent tax filing
>>> last_filing = org.filings_with_data[0]

# check the filing period
>>> last_filing.tax_prd
201912

# get total revenue for that year
>>> last_filing.totrevenue
1138297

# get organizations by state
>>> orgs = np.search.get(state='CA')
>>> orgs.organizations[1].name
'1 DREAM FOUNDATION INC'

# get organizations by keyword
>>> orgs = np.search.get(q='science', state='CA')
>>> orgs.total_results
566

>>> orgs.organizations[0].name
'SCIENCE CONNECTED'

# the ProPublica Nonprofit Explorer API returns 1 page of results per query.
# to iterate all organizations, use the .all_organizations() function, which
# returns a python generator. This will query each page sequentially.
>>> len(orgs.organizations)
100

>>> len(list(orgs.all_organizations()))
566

# This can generate a lot of API queries! Please be careful with this, and respectful of ProPublica's terms of use.


# query by multiple parameters (q, state, c_code, ntee)
>>> orgs = np.search.get(c_code=2, ntee=7)
>>> orgs.organizations[0].name
'100 SOUTH SWAN STREET REALTY CORP'

# use fetch to access endpoints directly
>>> orgs = np.fetch('search.json?q=delta')
>>> orgs.total_results
12490

# optionally use a custom lambda to parse results
>>> orgs = np.fetch('search.json?q=delta', lambda orgs: orgs.organizations[5])
>>> orgs.name
'DELTA DELTA DELTA'

```


[]: https://github.com/amoffatt/propublica-nonprofit/
