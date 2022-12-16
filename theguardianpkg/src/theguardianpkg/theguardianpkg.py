import requests
import pandas as pd
import os
import json
from json import dumps, loads
from pandas import json_normalize
from matplotlib import pyplot as plt
from ak import key
import seaborn as sns

def search(keyword, page=1, order='newest', page_size=50, lang='en'):
    """
    Searches for results based on keyword and other designated parameters.
    
    Parameters
    ----------
    keyword : str
        A string for the keyword you want to search.
    page: int
        An integer for which page to search from.
    order: str
        A string for how results should be ordered ('newest', 'oldest', 'relevance').
    page_size: int
        An integer for how many results should show up on each page.
    lang: str
        A string for which language results should be in, using ISO language codes.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        The new pandas dataframe showing the title, section, date, and type of the results.
        
    Examples
    --------
    >>> from guardianpkg import guardianpkg
    >>> guardianpkg.search('sport')
    >>> Output is dataframe with 50 most recent results with the keyword 'sport'
    >>> Refer to .ipynb file for example output
    """
    params = {'api-key':key, 
              'q':keyword, 
              'page':page,
              'order-by':order,
              'page-size':page_size, 
              'lang':lang}
    url = 'http://content.guardianapis.com/search?'
    r = requests.get(url, params=params)
    response = r.json()
    
    rr = []
    for r in response['response']['results']:
        result = {}
        result['title'] = r['webTitle']
        result['section'] = r['sectionName']
        result['date'] = r['webPublicationDate']
        result['type'] = r['type']
        rr.append(result)
    
    rdf = pd.DataFrame(rr)
    return rdf

def search_pages(keyword, pages=100, order='newest', page_size=50, lang='en'):
    """
    Searches for results based on keyword and other designated parameters, looping over multiple pages.
    
    Parameters
    ----------
    keyword : str
        A string for the keyword you want to search.
    pages: int
        An integer for how many pages to search from.
    order: str
        A string for how results should be ordered ('newest', 'oldest', 'relevance').
    page_size: int
        An integer for how many results should show up on each page.
    lang: str
        A string for which language results should be in, using ISO language codes.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        The new pandas dataframe showing the title, section, date, and type of the results.
        
    Examples
    --------
    >>> from guardianpkg import guardianpkg
    >>> guardianpkg.search_pages('book')
    >>> Output is dataframe most recent results with the keyword 'book' for 99 pages.
    >>> Refer to .ipynb file for example output
    """
    allr =[]
    for i in range(1, pages):
        page = i
        params = {'api-key':key, 
                  'q':keyword,
                  'page':i,
                  'page-size':page_size,
                  'lang':lang}
        url = 'http://content.guardianapis.com/search?'
        responses = requests.get(url, params)
        responses = responses.json()
        responses = responses['response']
        rrr = []
        for r in responses:
            results = responses['results']
            for r in results:
                result = {}
                result['title'] = r['webTitle']
                result['section'] = r['sectionName']
                result['date'] = r['webPublicationDate'][:7]
                result['type'] = r['type']
                allr.append(result)
        rdf = pd.DataFrame(allr)
    return rdf

def tags(tag_text, page=1, page_size=50):
    """
    Searches for all tags based on designated parameters.
    
    Parameters
    ----------
    tag_text : str
        A string for the included text for tags you want to search.
    page: int
        An integer for which page to search from.
    page_size: int
        An integer for how many results should show up on each page.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        The new pandas dataframe showing the name and type of the tag results.
        
    Examples
    --------
    >>> from guardianpkg import guardianpkg
    >>> guardianpkg.tags('liverpool')
    >>> Output is dataframe with tag results for 'liverpool'
    >>> Refer to .ipynb file for example output
    """
    params = {'api-key':key, 
              'web-title':tag_text,
              'page':page,
              'page-size':page_size}
    url = 'http://content.guardianapis.com/tags?'
    r = requests.get(url, params=params)
    response = r.json()
    
    rr = []
    for r in response['response']['results']:
        result = {}
        result['tag'] = r['webTitle']
        result['type'] = r['type']
        rr.append(result)
    
    rdf = pd.DataFrame(rr)
    return rdf

def section(section_text, page=1, page_size=50):
    """
    Searches for all sections based on designated parameters.
    
    Parameters
    ----------
    section_text : str
        A string for included text for the sections you want to search.
    page: int
        An integer for which page to search from.
    page_size: int
        An integer for how many results should show up on each page.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        The new pandas dataframe showing the name and type of the section results.
        
    Examples
    --------
    >>> from guardianpkg import guardianpkg
    >>> guardianpkg.section('liverpool')
    >>> Output is dataframe with results with the tag including 'liverpool'
    >>> Refer to .ipynb file for example output
    """
    params = {'api-key':key, 
              'q':section_text, 
              'page':page,
              'page-size':page_size}
    url = 'http://content.guardianapis.com/sections?'
    r = requests.get(url, params=params)
    response = r.json()
    
    rr = []
    for r in response['response']['results']:
        result = {}
        result['section'] = r['webTitle']
        rr.append(result)
    
    rdf = pd.DataFrame(rr)
    return rdf

def edition(edition_text):
    """
    Searches for all editions based on designated parameters.
    
    Parameters
    ----------
    edition_text : str
        A string for included text for the edition you want to search.
    page: int
        An integer for which page to search from.
    page_size: int
        An integer for how many results should show up on each page.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        The new pandas dataframe showing the name and type of the edition results.
        
    Examples
    --------
    >>> from guardianpkg import guardianpkg
    >>> guardianpkg.edition('uk')
    >>> Output is dataframe with results with the edition including 'uk'
    >>> Refer to .ipynb file for example output
    """
    params = {'api-key':key, 
              'q':edition_text}
    url = 'http://content.guardianapis.com/editions?'
    r = requests.get(url, params=params)
    response = r.json()
    
    rr = []
    for r in response['response']['results']:
        result = {}
        result['edition'] = r['webTitle']
        rr.append(result)
    
    rdf = pd.DataFrame(rr)
    return rdf

def item_url(keyword, page=1, order='newest', page_size=50, lang='en'):
    """
    Searches for API url for a result based on the designated parameters.
    
    Parameters
    ----------
    keyword : str
        A string for the keyword you want to search.
    page: int
        An integer for which page to search from.
    order: str
        A string for how results should be ordered ('newest', 'oldest', 'relevance').
    page_size: int
        An integer for how many results should show up on each page.
    lang: str
        A string for which language results should be in, using ISO language codes.
    
    Returns
    -------
    str
        The string for the API url of the result.
        
    Examples
    --------
    >>> from guardianpkg import guardianpkg
    >>> guardianpkg.item_url('film')
    'https://content.guardianapis.com/film/2022/dec/15/obituaries-2022-olivia-newton-john-remembered-by-didi-conn-frenchy-sandy-grease'
    """

    params = {'api-key':key, 
              'q':keyword, 
              'page':page,
              'order-by':order,
              'page-size':page_size, 
              'lang':lang}
    url = 'http://content.guardianapis.com/search?'
    r = requests.get(url, params=params)
    response = r.json()
    
    rr = []
    for r in response['response']['results']:
        result = {}
        result['title'] = r['webTitle']
        result['api_url'] = r['apiUrl']
        rr.append(result)
    
    rdf = pd.DataFrame(rr)
    return rdf['api_url'][0]

def single_item_mult(api_url):
    """
    Searches for a single result for an API url.
    
    Parameters
    ----------
    api_url : str
        A string for the API url for the result you want to search for.

    Returns
    -------
    str
        The resulting string including the title, section, date, and type of the result.
        
    Examples
    --------
    >>> from guardianpkg import guardianpkg
    >>> guardianpkg.single_item_mult('https://content.guardianapis.com/film/2022/dec/15/best-films-of-2022-in-the-uk-no-7-rrr')
    Title: Best films of 2022 in the UK: No 7 – RRR 
    Section: Film 
    Date: 2022-12-15T06:00:14Z 
    Type: article
    """
    params = {'api-key':key,
             'id':api_url}
    r = requests.get(api_url, params=params)
    response = r.json()
    output = response['response']['content']
    title = output['webTitle']
    section = output['sectionName']
    date = output['webPublicationDate']
    atype = output['type']

    return print(('Title: {}').format(title), '\n',
                ('Section: {}').format(section), '\n',
                ('Date: {}').format(date), '\n',
                ('Type: {}').format(atype))

def single_item(api_url):
    """
    Searches for result title based on API url.
    
    Parameters
    ----------
    api_url : str
        A string for API url you want to search.
    
    Returns
    -------
    str
        The string for the title of the result.
        
    Examples
    --------
    >>> from guardianpkg import guardianpkg
    >>> guardianpkg.single_item('https://content.guardianapis.com/film/2022/dec/15/obituaries-2022-olivia-newton-john-remembered-by-didi-conn-frenchy-sandy-grease')
    'Olivia Newton-John remembered by Didi Conn'
    """
    params = {'api-key':key,
             'id':api_url}
    r = requests.get(api_url, params=params)
    response = r.json()
    output = response['response']['content']
    title = output['webTitle']
    
    return title

def search_hist(x, order='newest', page_size=50, lang='en'):
    """
    Creates histogram to look at either types or pillars of results based on designated parameters.
    
    Parameters
    ----------
    x : str
        A string for which column of the search dataframe to plot (either 'type' or 'pillar').
    order: str
        A string for how results should be ordered ('newest', 'oldest', 'relevance').
    page_size: int
        An integer for how many results should show up on each page.
    lang: str
        A string for which language results should be in, using ISO language codes.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        The new pandas dataframe showing the name, section, date, type, and pillar of the results.
    matplotlib.axes._subplots.AxesSubplot
        A histogram showing distribution of designated variable among results.
        
    Examples
    --------
    >>> from guardianpkg import guardianpkg
    >>> guardianpkg.search_hist('pillar')
    >>> Output is dataframe with recent results and histogram showing distribution of pillars among these results.
    >>> Refer to .ipynb file for example output
    """

    params = {'api-key':key,
              'order-by':order,
              'page-size':page_size, 
              'lang':lang}
    url = 'http://content.guardianapis.com/search?'
    r = requests.get(url, params)
    response = r.json()
    
    rr = []
    for r in response['response']['results']:
        result = {}
        result['title'] = r['webTitle']
        result['section'] = r['sectionName']
        result['date'] = r['webPublicationDate']
        result['type'] = r['type']
        result['pillar'] = r['pillarName']
        rr.append(result)
    
    rdf = pd.DataFrame(rr)
    x = rdf[x]
    sns.histplot(data=x)
    
    return rdf
    return plot

def search_plot_template(x, y, hue, order='newest', page_size=50, lang='en'):
    """
    Creates a personalizable plot based on designated parameters.
    
    Parameters
    ----------
    x : str
        A string for the variable you want on the x-axis.
    y : str
        A string for the variable you want on the y-axis.
    hue: str
        A string for the variable you want for color-coding the points.
    page_size: int
        An integer for how many results should show up on each page.
    lang: str
        A string for which language results should be in, using ISO language codes.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        The new pandas dataframe showing the name, section, date, and type of the results.
    matplotlib.axes._subplots.AxesSubplot
        A scatterplot showing distribution of designated variables among results.
    
    Examples
    --------
    >>> from guardianpkg import guardianpkg
    >>> guardianpkg.search_plot_template('date', 'section', 'type')
    >>> Output is dataframe with recent results and scatterplot showing date, section, and type among these results.
    >>> Refer to .ipynb file for example output
    """

    params = {'api-key':key,
             'order-by':order,
             'page-size':page_size,
             'lang':lang}
    url = 'http://content.guardianapis.com/search?'
    r = requests.get(url, params)
    response = r.json()
    
    rr = []
    for r in response['response']['results']:
        result = {}
        result['title'] = r['webTitle']
        result['section'] = r['sectionName']
        result['date'] = r['webPublicationDate']
        result['type'] = r['type']
        rr.append(result)
    
    rdf = pd.DataFrame(rr)
    
    x1 = rdf[x]
    y1 = rdf[y]
    hue1 = rdf[hue]
    sns.scatterplot(x=x1, y=y1, hue=hue1)
    
    return rdf
    return plt.show()
