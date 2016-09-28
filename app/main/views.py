from flask import render_template, redirect, url_for, abort, flash, request,current_app, make_response
from flask_login import login_user, logout_user,login_required, current_user
from .. import db
from ..models import Permission, Role, User, Post
from ..email import send_email
from . import main
from .forms import PostForm,EditForm,LoginForm,ChangePasswordForm


@main.route('/', methods=['GET', 'POST'])
def index():
    post_form = PostForm()
    '''
    print('current_user', current_user)
    print('current_user._get_current_object()',current_user._get_current_object())
    if current_user.can(Permission.WRITE_ARTICLES) and post_form.data['submit']:
        post = Post(title=post_form.title.data,summary=post_form.summary.data,body=post_form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        #print('url_for(.index)',url_for('.index'))
        return redirect(url_for('.index'))
    if post_form.data['cancel']:
        return redirect(url_for('.index'))
    '''
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    return render_template('index.html', post_form=post_form, posts=posts, pagination=pagination)


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    post_form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and post_form.data['submit']:
        post = Post(title=post_form.title.data,summary=post_form.summary.data,body=post_form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    if post_form.data['cancel']:
        return redirect(url_for('.create'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        query = Post.query

    return render_template('create.html', post_form=post_form)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    edit_form = EditForm()
    if edit_form.data['submit']:
        post.title = edit_form.title.data
        post.summary = edit_form.summary.data
        post.body = edit_form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.index', id=post.id))
    if edit_form.data['delete']:
        db.session.delete(post)
        flash('The post has been delete.')
        return redirect(url_for('.index'))
        #return render_template('edit_post.html', form=form,delete_form=delete_form)
    if edit_form.data['cancel']:
        return redirect(url_for('.index'))

    edit_form.title.data = post.title
    edit_form.summary.data = post.summary
    edit_form.body.data = post.body
    return render_template('edit_post.html', edit_form=edit_form)



@main.route('/blog/<int:id>', methods=['GET', 'POST'])
def blog(id):
    post = Post.query.get_or_404(id)
    '''
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = EditForm()
    form.title.data = post.title
    form.body.data = post.body
    '''
    return render_template('blog.html', post=post)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('.index'))
        else:
            flash('Invalid password.')
    return render_template("change_password.html", form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))