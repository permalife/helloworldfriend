from setuptools import setup

setup(name='helloworldfriend',
      version='0.1',
      description='Django app for time-delayed friend greeting',
      url='http://github.com/nickolashe/greetfrienddelay',
      author='Nickolay Shestopalov',
      author_email='nicko.shestopalov@gmail.com',
      packages=['helloworld'],
      install_requires=[
          'Django>=1.8.6',
          'gunicorn>=19.3.0',
          'celery>=3.1.19',
          'supervisor>=3.1.3',
          # rabbitmq-server
      ],
      zip_safe=False)
