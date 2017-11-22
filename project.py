from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
from database_setup import Category, Option, Link
from flask import session as login_session
from signin import doSignout, fbConnect, returnUserId, signin_required
from common import session, meta_title, meta_desc, meta_url
from common import get_cats, get_cat_by_name, get_options_by_cat
from common import get_option_by_id, get_option_by_name, update_option
from common import get_links_by_opId, get_link_by_id
# app name
app = Flask(__name__)


@app.route('/')
def main():
    log = str(login_session.has_key('username'))
    return render_template('main.html', meta_title=meta_title,
                           meta_desc=meta_desc,
                           log=log, categories=get_cats())


@app.route('/signin')
def signin():
    log = str(login_session.has_key('username'))
    return render_template('signin.html', meta_title=meta_title,
                           meta_desc=meta_desc, log=log,
                           categories=get_cats())


@app.route('/signout')
def signout():
    global log
    log = doSignout()
    return redirect(url_for('main'))


@app.route('/fbsignin', methods=['POST'])
def fbsignin():
    global log
    log = fbConnect()
    return 'Success'


# caegory
@app.route('/<string:category_name>')
def category(category_name):
    log = str(login_session.has_key('username'))
    category = get_cat_by_name(category_name)
    options = get_options_by_cat(category)
    return render_template('category.html', meta_title=meta_title,
                           meta_desc=meta_desc, log=log,
                           categories=get_cats(), category=category,
                           options=options)


# newOption
@app.route('/<string:category_name>/new', methods=['GET', 'POST'])
@signin_required
def newOption(category_name):
    log = str(login_session.has_key('username'))
    category = get_cat_by_name(category_name)
    if request.method == 'POST':
        # check if required fields are filled
        if request.form['name'] == '' or request.form['description'] == '':
            warning = "Fill both name and description to add  option"
            return render_template('new-option.html', category=category,
                                   categories=get_cats(), log=log,
                                   warning=warning)
        # create new option
        else:
            user_id = login_session['user_id']
            anotherOption = Option(name=request.form['name'],
                                   description=request.form['description'],
                                   cat_id=category.id, user_id=user_id)
            session.add(anotherOption)
            session.commit()
            return redirect(url_for('category', category_name=category.name))
    else:
        return render_template('new-option.html', category=category, categories=get_cats(), log=log)


# caegory
@app.route('/<string:category_name>/<int:option_id>')
def option(category_name, option_id):
    log = str(login_session.has_key('username'))
    category = get_cat_by_name(category_name)
    option = get_option_by_id(option_id)
    links = get_links_by_opId(option_id)
    return render_template('option.html', meta_title=meta_title,
                           meta_desc=meta_desc, log=log,
                           categories=get_cats(), category=category,
                           option=option, links=links)


@signin_required
@app.route('/<string:category_name>/<int:option_id>/edit',
           methods=['GET', 'POST'])
def editOption(category_name, option_id):
    log = str(login_session.has_key('username'))
    user_id = login_session['user_id']
    category = get_cat_by_name(category_name)
    option = get_option_by_id(option_id)
    links = get_links_by_opId(option_id)
    # check if obj in db
    if category and option:
        if request.method == 'POST':
            f = request.form
            if f['name'] == '' or f['description'] == '':
                warning = "You need both Research Option' and 'Description'"
                return render_template('edit-option.html', log=log,
                                       meta_title=meta_title,
                                       meta_desc=meta_desc,
                                       categories=get_cats(),
                                       category=category,
                                       option=option, links=links,
                                       warning=warning)
            else:
                update_option(option, f)
                category = session.query(Category).filter_by(id=option.cat_id).one()
                flash(option.name+' has updated')
                return redirect(url_for('option', category_name=category.name,
                                option_id=option.id))
        # show option page
        else:
            return render_template('edit-option.html', meta_title=meta_title,
                                   meta_desc=meta_desc, log=log,
                                   categories=get_cats(), category=category,
                                   option=option, links=links)


@signin_required
@app.route('/<string:category_name>/<int:option_id>/newlink', methods=['POST'])
def addLink(category_name, option_id):
    log = str(login_session.has_key('username'))
    user_id = login_session['user_id']
    option = get_option_by_id(option_id)
    f = request.form
    if f['link'] == '' or f['url'] == '':
        flash('You need both Link name and Url to add a new link')
    else:
        link = Link(title=f['link'], url=f['url'], option_id=option.id)
        session.add(link)
        session.commit()
    return redirect(url_for('editOption', category_name=category_name,
                            option_id=option_id))


@signin_required
@app.route('/<string:category_name>/<int:option_id>/delete')
def deleteOption(category_name, option_id):
    option = get_option_by_id(option_id)
    delete_name = option.name
    session.delete(option)
    session.commit()
    flash(delete_name + ' has been deleted.')
    return redirect(url_for('category', category_name=category_name))


@signin_required
@app.route('/<string:category_name>/<int:option_id>/<int:link_id>/delete')
def deleteLink(category_name, option_id, link_id):
    link = get_link_by_id(link_id)
    delete_name = link.title
    session.delete(link)
    session.commit()
    flash(delete_name + ' has been deleted.')
    return redirect(url_for('editOption', category_name=category_name,
                            option_id=option_id))


# return JSON
@app.route('/<string:category_name>/JSON')
def categoryJSON(category_name):
    category = get_cat_by_name(category_name)
    options = get_options_by_cat(category)
    return jsonify(Options=[i.serialize for i in options])


@app.route('/<string:category_name>/<int:option_id>/JSON')
def optionJSON(category_name, option_id):
    option = get_option_by_id(option_id)
    return jsonify(Option=option.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    # let hear any webserver
    app.run(host='0.0.0.0', port=5000)
