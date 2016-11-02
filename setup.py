import setuptools


setuptools.setup(name='py-poloniex',
                 version='0.3',
                 description='Python Poloniex API',
                 long_description=open('README.md').read().strip(),
                 author='Thiago Fernandes Macedo',
                 author_email='thiago@internetbudi.com.br',
                 url='https://github.com/thiagof/py-poloniex',
                 py_modules=['poloniex'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='poloniex bitcoin btc api exchange',
                 classifiers=[
                    # How mature is this project? Common values are
                    #   3 - Alpha
                    #   4 - Beta
                    #   5 - Production/Stable
                    'Development Status :: 4 - Beta',

                    # Indicate who your project is intended for
                    'Intended Audience :: Developers',
                    'Topic :: Software Development :: Bitcoin',

                    # Pick your license as you wish (should match "license" above)
                     'License :: OSI Approved :: MIT License',

                    # Specify the Python versions you support here. In particular, ensure
                    # that you indicate whether you support Python 2, Python 3 or both.
                    'Programming Language :: Python :: 2.6',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3.3',
                    'Programming Language :: Python :: 3.4',
                    'Programming Language :: Python :: 3.5',
                ])

