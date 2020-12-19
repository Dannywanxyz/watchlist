from watchlist.models import Article, Movie, User
from watchlist import admin, db
from flask_admin.contrib.sqla import ModelView


class UserView(ModelView):
    """docstring for UserView"""
    can_create = False
    can_edit = False
    can_delete = False
    column_exclude_list = ['password_hash']
    column_editable_list = ['username']


admin.add_view(UserView(User, db.session, name="用户管理"))
admin.add_view(ModelView(Article, db.session, name="文章管理"))
admin.add_view(ModelView(Movie, db.session, name="电影管理"))
