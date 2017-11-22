from flask import Flask, flash, request, redirect, url_for
from database_setup import Base, User
from flask import session as login_session
import httplib2
import json
from common import session, FB_ID, FB_SCRT


def signin_required(func):
    """
    A decorator to confirm a user is signed in or redirect as needed.
    """
    def check_signin(*args, **kwargs):
        # Redirect to login if user not logged in, else execute func.
        if login_session.has_key('username'):
            return func(*args, **kwargs)
        else:
            flash('Sign in to add new, edit, or delete the post')
            return redirect(url_for('signin'))
    return check_signin


def fbDisconnect():
    facebook_id = login_session['provider_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


def doSignout():
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbDisconnect()
        del login_session['access_token']
        del login_session['provider_id']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['provider']
        flash("You have been signed out")
    global log
    log = 'False'
    return log


def fbConnect():
    access_token = request.data
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (FB_ID, FB_SCRT, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    ''' 
        Due to the formatting for the result from the server token exchange 
        we have to split the token first on commas and select the first
        index which gives us the key : value for the server access token 
        then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can 
        be used directly in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['access_token'] = token
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['provider_id'] = data["id"]
    login_session['user_id'] = returnUserId(login_session)
    global log
    log = 'True'
    return log


# User Helper Functions
def createUser(login_session):
    ''' register the user and return the user id'''
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def returnUserId(login_session):
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    return user_id


