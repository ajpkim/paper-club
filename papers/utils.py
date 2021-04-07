import random
import urllib
import urllib.request as libreq
import re

import feedparser

from .models import Author, AuthorPaper, Paper


# TODO handle unique authors with same name
def process_arxiv_data(data):
    """
    Process the cleaned arXiv API data by fetching existing database
    items or creating new ones.
    
    Returns tuple of Paper and Author list matching given data.
    """
    authors = [Author.objects.get(name=name) if
               Author.objects.filter(name=name).exists() else
               Author.objects.create(name=name) for
               name in data.authors]
    
    if Paper.objects.filter(arxiv_id=data['arxiv_id']).exists():
        paper = Paper.objects.get(arxiv_id=data['arxiv_id'])
    else:
        paper = Paper.objects.create(url=data.url,
                                     pdf_url=data.pdf_url,
                                     arxiv_id = data.arxiv_id,
                                     title=data.title,
                                     abstract=data.summary,
                                     published=data.published,
                                     )
        # Only create AuthorPaper ManyToMany if creating a new Paper
        for author in authors:
            AuthorPaper.objects.create(author=author, paper=paper)
        
    return paper, authors


def clean_arxiv_paper_data(data):

    def remove_new_lines(s):
        pat = r"\n( )*"
        s = re.sub(pat, " ", s)
        return s    

    data.title = remove_new_lines(data.title)
    data.summary = remove_new_lines(data.summary)
    data.published = data.published.split("T")[0]  # Convert "2021-02-02T04:07:38Z" to "%Y-%m-%d"
    data.authors = [author['name'] for author in data.authors]
    return data

def get_arxiv_paper_data(url):
    """
    Query the arXiv.org API to retrieve metadata on the paper given by
    the url and return augmented data in a feedparser dict.
    
    - url: is a url to a paper hosted at  arxiv.org
      e.g. "https://arxiv.org/abs/cond-mat/0207270v3".
    """
    base, page_type, arxiv_id = re.split('(abs/|pdf/){1}', url)
    if page_type == 'pdf/':
        arxiv_id = arxiv_id[:-4]  # strip the ".pdf" suffix
    query = base +'api/query?id_list=' + arxiv_id
    response = libreq.urlopen(query)
    feed = feedparser.parse(response)
    data = feed.entries[0]
    data['arxiv_id'] = arxiv_id
    data['url'] = base + 'abs/' + arxiv_id
    data['pdf_url'] = base + 'pdf/' + arxiv_id + '.pdf'
    return clean_arxiv_paper_data(data)

def process_paper_url(url):
    data = get_arxiv_paper_data(url)
    paper, authors = process_arxiv_data(data)
    return paper, authors


def generate_random_arxiv_url():
    """
    Info on arXiv identifiers: https://arxiv.org/help/arxiv_identifier
    """
    year = str(random.randint(2008, 2020))[2:]
    month = random.randint(1,12)
    month = "0" + str(month) if month < 10 else str(month)
    id_num = str(random.randint(0, 5000))
    id_size = 5 if int(year) < 15 else 4  # dictates number of leading zeros
    while len(id_num) < id_size:
        id_num = "0" + id_num
        
    return f"https://arxiv.org/abs/{year + month}.{id_num}"
    
def get_random_arxiv_paper():
    url = generate_random_arxiv_url()

    while True:
        try:
            paper, authors = process_paper_url(url)
            break
        except urllib.error.HTTPError:
            print('\n\nhahaha\n\n')
            url = get_random_arxiv_paper() 

    return paper
