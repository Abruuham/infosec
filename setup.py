from setuptools import setup


def readme_content():
    with open('README.rst') as readme_file:
        data = readme_file.read()
    return data


setup(
    name='stinger',
    version='1.0.0',
    description='Simple Honeypot logging',
    long_description=readme_content(),
    author='Abraham',
    author_email='abrahamcalvillo@ymail.com',
    license='MIT',
    packages=['stinger'],
    zip_safe=False,
    install_requires=[
        'twisted',
        'paramiko',
        'ipinfo',
        'yaml'
    ]
)
