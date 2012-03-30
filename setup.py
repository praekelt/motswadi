from setuptools import setup, find_packages

setup(
    name='motswadi',
    version='0.0.1',
    description='Parent education involvement through mobile messaging.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/motswadi',
    packages = find_packages(),
    dependency_links = [
        'https://github.com/praekelt/vumi/zipball/develop#egg=vumi',
    ],
    install_requires=[
        'django',
        'django-snippetscream',
        'psycopg2',
        'south',
        'vumi',
    ],
    tests_require=[
        'django-setuptest',
    ],
    test_suite="setuptest.SetupTestSuite",
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
