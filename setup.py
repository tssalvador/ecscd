from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='ecscd',
      version='0.1',
      description='ECS application deploy manage',
      packages=['ecscd'],
      url='http://www.ebanx.com',
      author='Egon Braun',
      author_email='ops@ebanx.com',
      entry_points={
          'console_scripts': ['ecscd=ecscd.ecscd:main'],
      },
      include_package_data=True,
      zip_safe=False)
