from flask import Flask, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Option, Link
import json

# sqlalchemy to access db
engine = create_engine('sqlite:///researchoption.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# common info
meta_title = 'Design Research'
meta_desc = '''Design research resources and
               links for projects.'''
meta_url = 'URL_MAIN'

# for fb login
FB_ID = json.loads(open('fb_client.json', 'r').read())['web']['app_id']
FB_SCRT = json.loads(open('fb_client.json', 'r').read())['web']['app_secret']


# Helpers
def get_cat_by_name(category_name):
    category_name = category_name.lower().title()
    category = session.query(Category).filter_by(name=category_name).one()
    return category


def get_cats():
    return session.query(Category).all()


def get_options_by_cat(category):
    options = session.query(Option).filter_by(cat_id=category.id).all()
    return options


# get an option
def get_option_by_id(option_id):
    option = session.query(Option).filter_by(id=option_id).one()
    return option


def get_option_by_name(option_name):
    option_name = option_name.lower().title()
    option = session.query(Option).filter_by(name=option_name).one()
    category = session.query(Category).filter_by(id=option.cat_id).one()
    return option, category


# return link list
def get_links_by_opId(option_id):
    links = session.query(Link).filter_by(option_id=option_id).all()
    return links


def get_link_by_id(link_id):
    link = session.query(Link).filter_by(id=link_id).one()
    return link


def update_option(option, request_form):
    # check option name
    f = request_form
    given_name = f['name']
    if given_name != option.name:
        option.name = given_name
    # check category name
    given_cat = f['cat']
    if given_cat != option.cat_id:
        option.cat_id = given_cat
    # check description
    given_desc = f['description']
    if given_desc != option.description:
        option.description = given_desc
    # get link list
    link_list = []
    for key in f.keys():
        if "linkUrl" in key:
            link_list.append(key[8:])
    for link_num in link_list:
        given_link = f['link-'+link_num]
        given_url = f['linkUrl-'+link_num]
        # update existing links
        link = session.query(Link).filter_by(id=int(link_num)).one()
        if given_link != link.title:
            link.title = given_link
        if given_url != link.url:
            link.url = given_url
        session.add(link)
    session.add(option)
    session.commit()

