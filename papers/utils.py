import pdb
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


########## arXiv API functions ##########
def clean_arxiv_paper_data(data):

    def remove_new_lines(s):
        pat = r"\n( )*"
        s = re.sub(pat, " ", s)
        return s    

    data.title = remove_new_lines(data.title)
    data.summary = remove_new_lines(data.summary)
    # Convert "YYYY-MM-DDTHH:MM:SSZ" to "YYYY-MM-DD"
    data.published = data.published[0:9]
    # Extract author names
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
    
