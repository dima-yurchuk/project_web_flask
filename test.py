from flask_testing import TestCase
import unittest
# from app import create_app, db
from app.profile.models import User
from app.task.models import Task
from flask import current_app as app


class TestApp(TestCase):
    def create_app(self):
        # app = create_app()
        # let's use SQLite3 as it is much faster to test with than a larger postgres DB
        #app.config.from_object('config.TestConfiguration')
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///form.db'
        return app

    def test_main_page(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # def test_register(self):
    #     user = User(username='test333', email='test333@gmail.com', password='11111111')
    #     db.session.add(user)
    #     db.session.commit()
    # def test_login(self): # ????????????????????????????????????????????????????????????????????
    #     response = self.client.post(
    #         '/auth/login2',
    #         data=dict(email="test333@gmail.com", password="11111111"),
    #         follow_redirects=True
    #     )
    #     self.assertEqual(response.status_code, 200)
    # def test_logout(self): # ???????????????????????????????????????????????????????????????????
    #     self.client.post(
    #         '/auth/login2',
    #         data=dict(email="test333@gmail.com", password="11111111"),
    #         follow_redirects=True
    #     )
    #     response = self.client.get('/auth/logout', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)


    # def test_task_create(self):
    #     response = self.client.post(
    #         '/api/v2/tasks',
    #         data=dict(title="Title333", description="Description333", priority="low", category_id=1),
    #         follow_redirects=True
    #     )
    #     self.assertIn(b'Data add in db!', response.data)

    # def test_task_show(self): # ??????????????????????????????????????????????????????????????????
    #     response = self.client.get(
    #         '/api/v2/tasks/86',
    #         follow_redirects=True
    #     )
    #     self.assertEqual(response.json, dict(resource=dict(id=86, title="Title333", description="Description333", created="2021-05-30", priority="MyEnum.low", is_done=False)))

    # def test_task_update(self):
    #     task = Task.query.filter_by(id=86).first()
    #     response = self.client.put(
    #         '/api/v2/tasks/86',
    #         data=dict(title="Title333m", description="Description333m", created="Tue, 11 May 2021 12:00:00 GMT",  priority="low", is_done='True', category_id=1),
    #         follow_redirects=True
    #     )
    #     self.assertIn(b'Task succesfully update!', response.data)

    # def test_task_delete(self):
    #     response = self.client.delete(
    #         '/api/v2/tasks/86',
    #         # data=dict(id=86),
    #         follow_redirects=True
    #     )
    #     self.assertIn(b'The task has been deleted', response.data)

if __name__== "__main__":
    unittest.main()