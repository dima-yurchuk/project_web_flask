import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'asfdsfsaaffdf'
WTF_CRSF_ENAVLED = True
# Database
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'form.db')
SQLALCHEMY_DATABASE_URI =  'postgres://yijbkrgthkzeou:d1a94533fb6656b607c35ed88d083750f86686519b4d8c6d782387dc32bd7e8a@ec2-54-228-99-58.eu-west-1.compute.amazonaws.com:5432/d15pdg7da4lr08'
SQLALCHEMY_TRACK_MODIFICATIONS = False