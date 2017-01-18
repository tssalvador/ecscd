from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='ecscd',
      version='0.1',
      description='Command line application and library to assist on continuous delivery for Amazon AWS\' EC2 Container Service',
      packages=['ecscd'],
      url='https://github.com/egonbraun/ecscd',
      author='Egon Braun',
      author_email='egon@ohbyteme.com',
      entry_points={
          'console_scripts': ['ecscd=ecscd.ecscd:main'],
      },
      include_package_data=True,
      zip_safe=False)
