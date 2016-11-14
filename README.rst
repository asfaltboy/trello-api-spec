Trello API spec
===============

This project consists of a simple scraper (based on scrapy) and a RAML generator (mapping scraper results to match required format).

Requires:
  - Python 3.5
  - Scrapy

Running scraper locally
-----------------------

1. First change the working dir to the scraper dir: ``cd API-Docs-Scraper/``
2. Serve test files in current directory with ``python -m http.server``.
3. In another shell process, scrape the local files with ``scrapy crawl api-docs -t json -o result.json``

Running scraper remotely
------------------------

1. First change the working dir to the scraper dir: ``cd API-Docs-Scraper/``
2. Change the ``start_urls`` attribute of ``ApiDocsSpider`` in ``trello/spiders/api_docs.py`` to the remote urls rather then local ones.
3. Scrape the remote files with ``scrapy crawl api-docs -t json -o result.json``

TODO
####

This is still a work in progress, and a few things are required for this to be complete::

  * [ ] Map scraper output to RAML spec format
  * [ ] Test all the endpoints
  * [ ] Parse other properties:
    - [ ] Examples
    - [ ] Permissions
  * [ ] Support authentication
  * [ ] Support argparse driven local/remote toggle
