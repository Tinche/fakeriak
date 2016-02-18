from setuptools import find_packages, setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='fakeriak',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/Tinche/fakeriak',
    license='Apache 2.0',
    author='Tin Tvrtkovic',
    author_email='tinchester@gmail.com',
    description='Library for testing code that uses Riak.',
    long_description=readme,
    install_requires=[
        'riak >= 2.2.0',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Testing",
    ],
)
