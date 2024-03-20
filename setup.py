from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fd:
    readme = fd.read()

with open('requirements.txt', encoding='utf-8') as fd:
    requirements = fd.read()

with open('requirements-dev.txt', encoding='utf-8') as fd:
    requirements_dev = fd.read()

setup(
    name='loadtest',
    version='0.1.0',
    description="Load testing benchmark tool",
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=requirements,
    extra_requires=requirements_dev,
)
