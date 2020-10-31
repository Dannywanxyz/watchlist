import click
from watchlist import app, db
from watchlist.models import Movie, User


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialize Database.')


@app.cli.command()
def forge():
    """生成假数据"""
    db.create_all()
    name = 'Nathon Drake'
    movies = [
        # {'title':'Forist Gump', 'year':'1991'}
        {'title': 'Iron Man', 'year': '2008'},
        {'title': 'Incredible Hulk', 'year': '2008'},
        {'title': 'Captain America', 'year': '2008'},
        {'title': 'Thor', 'year': '2010'},
        {'title': 'Avengers', 'year': '2012'},
        {'title': 'Captain America:Cival War', 'year': '2015'},
        {'title': 'Blank Panther', 'year': '2017'},
        {'title': 'Avengers:Infinity War', 'year': '2018'},
        {'title': 'Captain Marvel', 'year': '2019'},
        {'title': 'Avengers:End Game', 'year': '2019'}
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done!')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login')  # noqa: E501
def admin(username, password):
    """ Create User"""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')
