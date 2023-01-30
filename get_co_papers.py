#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import bibtexparser

import logging

import uk_dir

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s: %(message)s', level=logging.INFO)

class Papers(object):
    def __init__(self, bibfile):
        with open(bibfile) as fi:
            self.db = bibtexparser.load(fi)
            #self.df = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(bibfile)

        log.info("loaded bibtex file: {}".format(bibfile))

    def _get_dir_authors(self, authors):
        counter = 0
        dir_authors = []
        for author in authors:
            if author in uk_dir.dir_authors:
                dir_authors.append(author)
                counter = counter + 1
        return dir_authors

    def _get_volume(self, db_entry):
        try:
            return db_entry["volume"]
        except:
            log.debug("volume not defined for {}".format(db_entry["title"]))
            return ''

    def _get_number(self, db_entry):
        try:
            return db_entry["number"]
        except:
            log.debug("number not defined for {}".format(db_entry["title"]))
            return ''

    def _get_pages(self, db_entry):
        try:
            return db_entry["pages"]
        except:
            log.debug("volume not defined for {}".format(db_entry["title"]))
            return ''

    def _get_issue(self, db_entry):
        try:
            return db_entry["issue"]
        except:
            log.debug("issue not defined for {}".format(db_entry["title"]))
            return ''

    def _get_doi(self, db_entry):
        try:
            return db_entry["article-doi"]
        except:
            log.debug("doi not defined for {}".format(db_entry["title"]))
            return ''

    def _test_first(self, authors):
        if authors[0] in own_names:
            return 1
        else:
            return 0

    def _test_last(self, authors):
        if authors[-1] in own_names:
            return 1
        else:
            return 0

    def create_list(self):
        filter_dc = {}
        for idx, e in enumerate(self.db.entries):
            authors = [author.strip() for author in e["author"].split(" and ")]
            dir_authors = self._get_dir_authors(authors)
            #journal = e["title-abbreviation"]
            journal = e["journal"]
            title = e["title"]
            volume = self._get_volume(e)
            pages = self._get_pages(e)
            number = self._get_issue(e)
            issue = self._get_issue(e)
            doi = self._get_doi(e)
            n_authors = len(authors)
            n_dir_authors = len(dir_authors)
            last_authorship = self._test_last(authors)
            first_authorship = self._test_first(authors)

            filter_dc[idx] = {"journal": journal,
                              "title": title,
                              #"authors": " and ".join(authors), #this would be better
                              "authors": ", ".join(authors), #this f**s everything up
                              "dir_authors": ", ".join(dir_authors), #this f**s everything up
                              "volume": volume,
                              "issue": issue,
                              "number": number,
                              "pages": pages,
                              "doi": doi,
                              "n_authors": n_authors,
                              "n_dir_authors": n_dir_authors,
                              "last_authorship": last_authorship,
                              "first_authorship": first_authorship
                              }

        df = pd.DataFrame.from_dict(filter_dc, orient="index")
        return df



if __name__ == "__main__":
    bibfile = "papers_coauthor_2022.bib"
    p_2022 = Papers(bibfile)

    own_names = ["Nonnenmacher, Tobias", "Nonnenmacher, T."]
    tono = p_2022.create_list()

    save_file = "the_result.xlsx"
    tono.to_excel(save_file, index=False)
    log.info("saved results in {}".format(save_file))
    



