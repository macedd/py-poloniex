import setuptools
from packagename.version import Version


setuptools.setup(name='py-poloniex',
                 version=Version('1.0.0').number,
                 description='Python Poloniex API Wrapper',
                 long_description=open('README.md').read().strip(),
                 author='Thiago Fernandes Macedo',
                 author_email='thiago@internetbudi.com.br',
                 url='https://github.com/thiagof/py-poloniex',
                 py_modules=['poloniex'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='poloniex bitcoin btc api exchange',
                 classifiers=['Bitcoin', 'Api', 'Exchange'])
