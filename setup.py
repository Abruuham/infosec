from setuptools import setup


def readme_content():
    with open('README.rst') as readme_file:
        data = readme_file.read()
    return data


setup(
    name='HoneyPot',
    version='1.0.0',
    description='Simple HoneyPot',
    long_description=readme_content(),
    author='Abraham',
    author_email='abrahamcalvillo@ymail.com',
    license='MIT',
    packages=['honeypot'],
    zip_safe=False,
    install_requires=[]
)
