import unittest

from watchlist import app, db
from watchlist.commands import forge, initdb
from watchlist.models import Movie, User


class WatchListTestCase(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        # 创建数据库
        db.create_all()
        # 创建测试数据， 一个用户, 一个电影条目
        user = User(name='Test', username='test')  # 新建用户
        user.set_password('123')  # 设置密码
        movie = Movie(title='Test Movie Title', year='2020')  # 创建一条电影记录
        db.session.add_all([user, movie])     # add_all方法一次性传入多个模型类实例，以列表传入
        db.session.commit()

        self.client = app.test_client()  # 创建测试客户端
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库表

    # 测试程序实例是否存在
    def test_app_exist(self):
        self.assertIsNotNone(app)

    # 测试程序是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    # 开始测试客户端
    # 测试404页面

    def test_404_page(self):
        response = self.client.get('/nothing')  # 传入目标url
        data = response.get_data(as_text=True)
        # print(data)
        self.assertIn('Page Not Found - 404', data)
        self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)

    # 辅助方法，登陆用户
    def login(self):
        self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)

    # 测试创建条目
    def test_create_item(self):
        self.login()

        # 测试创建条目操作
        response = self.client.post('/', data=dict(
            title='New Movie',
            year='2020'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item Created', data)
        self.assertIn('New Movie', data)

        # 测试创建条目操作，但电影标题为空
        response = self.client.post('/', data=dict(
            title='',
            year='2020'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item Created', data)
        self.assertIn('Invalid input', data)

        # 测试创建条目操作， 但年份为空
        response = self.client.post('/', data=dict(
            title='New Movie',
            year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item Created', data)
        self.assertIn('Invalid input', data)

    # 测试更新条目
    def test_update_item(self):
        self.login()
        # 测试更新页面
        response = self.client.get('/movie/edit/1')
        data = response.get_data(as_text=True)
        # print(data)
        self.assertIn('Edit Item', data)
        self.assertIn('Test Movie Title', data)
        self.assertIn('2020', data)

        # 测试更新条目操作
        response = self.client.post('/movie/edit/1', data=dict(
            title='New Movie Edited',
            year='2021'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item Updated', data)
        self.assertIn('New Movie Edited', data)

        # 测试更新条目操作，标题为空
        response = self.client.post('/movie/edit/1', data=dict(
            title='',
            year='2021'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item Updated', data)
        self.assertIn('Invalid input', data)

        # 测试更新条目操作，年份为空
        response = self.client.post('/movie/edit/1', data=dict(
            title='New Movie Edited',
            year=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item Updated', data)
        self.assertIn('Invalid input', data)

    # 测试删除条目
    def test_delete_item(self):
        self.login()

        # 测试删除条目操作
        response = self.client.post('/movie/delete/1', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item deleted', data)
        self.assertNotIn('Test Movie Title', data)

    # 测试登陆保护
    def test_login_protect(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('<form method="POST">', data)

    # 测试登陆
    def test_login(self):
        response = self.client.post('/login', data=dict(
            username='test',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Login Success', data)
        self.assertIn('Logout', data)
        self.assertIn('Settings', data)
        self.assertIn('Edit', data)
        self.assertIn('Delete', data)
        self.assertIn('<form method="POST">', data)

        # 测试以错误的用户名登陆
        response = self.client.post('/login', data=dict(
            username='wrongtest',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login Success', data)
        self.assertIn('Invalid username or password', data)

        # 测试以错误的密码登陆
        response = self.client.post('/login', data=dict(
            username='test',
            password='wrongpw'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login Success', data)
        self.assertIn('Invalid username or password', data)

        # 测试以空的用户名登陆
        response = self.client.post('/login', data=dict(
            username='',
            password='123'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login Success', data)
        self.assertIn('Invalid input', data)

        # 测试以空的密码登陆
        response = self.client.post('/login', data=dict(
            username='test',
            password=''
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Login Success', data)
        self.assertIn('Invalid input', data)

    # 测试登出
    def test_logout(self):
        self.login()

        response = self.client.get('/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Goodbye', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('<form method="POST">', data)

    # 测试设置
    def test_settings(self):
        self.login()

        # 测试设置页面
        response = self.client.get('/settings', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Settings', data)
        self.assertIn('Your Name', data)

        # 测试更新设置
        response = self.client.post('/settings', data=dict(
            name='New Test Name',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Settings Updated', data)
        self.assertIn('New Test Name', data)

        # 测试更新设置，名称为空
        response = self.client.post('/settings', data=dict(
            name='',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Settings Updated', data)
        self.assertIn('Invalid input', data)

    # 测试命令
    # 测试虚拟数据
    def test_command(self):
        result = self.runner.invoke(forge)
        self.assertIn('Done', result.output)
        # movies = Movie.query.all()
        # print(movie.title for movie in movies)
        #     print(movie.title, movie.year)
        self.assertNotEqual(Movie.query.count(), 0)

    # 测试初始化数据库
    def test_initdb(self):
        result = self.runner.invoke(initdb)
        self.assertIn('Initialize Database.', result.output)

    # 测试建立管理员账户命令
    def test_create_admin_command(self):
        db.drop_all()
        db.create_all()
        result = self.runner.invoke(
            args=['admin', '--username', 'Nathon', '--password', '123'])
        self.assertIn('Creating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'Nathon')
        self.assertTrue(User.query.first().validate_password('123'))

    # 测试更新管理员账户命令
    def test_update_admin_command(self):
        result = self.runner.invoke(
            args=['admin', '--username', 'Nathon Drake', '--password', '456'])
        self.assertIn('Updating user...', result.output)
        self.assertIn('Done.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'Nathon Drake')
        self.assertTrue(User.query.first().validate_password('456'))


if __name__ == '__main__':
    unittest.main()
