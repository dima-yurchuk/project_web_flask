from flask_testing import TestCase
import unittest
from app import create_app, db
from app.profile.models import User
from app.task.models import Task
# from flask import current_app as app
unittest.TestLoader.sortTestMethodsUsing = None
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required

class TestApp(TestCase):
    def create_app(self):
        app = create_app()
        app.config.update(SQLALCHEMY_DATABASE_URI = 'sqlite:///form.db', SECRET_KEY = 'asfdsfsaaffdf')
        return app

    def test_a_main_page(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'PYTHON VESION', response.data)


    def test_b_auth(self):
        with self.client:
            user = User(username='test333', email='test333@gmail.com', password='11111111')
            db.session.add(user)
            db.session.commit()
            self.assertIn(db.session.query(User).filter_by(username='test333').first().email, 'test333@gmail.com')
            response = self.client.post(
                '/auth/login',
                data=dict(email="test333@gmail.com", password="11111111"),
                follow_redirects=True
            )
            user_in_db = User.query.filter(User.email == 'test333@gmail.com').first()
            login_user(user_in_db)
            self.assertIn(b'test333@gmail.com', response.data)
            self.assertEqual(current_user.is_authenticated, True)
            logout_user()
            self.assertEqual(current_user.is_authenticated, False)

    def test_c_task_create(self):
        response = self.client.post(
            '/api/v2/tasks',
            data=dict(title="Title333", description="Description333", priority="low", category_id=1),
            follow_redirects=True
        )
        self.assertIn(b'Data add in db!', response.data)

    def test_d_task_show(self): # ??????????????????????????????????????????????????????????????????
        response = self.client.get(
            '/api/v2/tasks/86',
            follow_redirects=True
        )
        self.assertEqual(response.json, dict(resource=dict(id=86, title="Title333", description="Description333", created=datetime.utcnow().strftime('%Y-%m-%d'), priority="MyEnum.low", is_done=False)))

    def test_e_task_update(self):
        response = self.client.put(
            '/api/v2/tasks/86',
            data=dict(title="Title333m", description="Description333m", created="Tue, 11 May 2021 12:00:00 GMT",  priority="low", is_done='True', category_id=1),
            follow_redirects=True
        )
        self.assertIn(b'Task succesfully update!', response.data)

    def test_f_task_delete(self):
        response = self.client.delete(
            '/api/v2/tasks/86',
            # data=dict(id=86),
            follow_redirects=True
        )
        self.assertIn(b'The task has been deleted', response.data)

if __name__== "__main__":
    unittest.main()