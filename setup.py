import pathlib
import setuptools

LONG_DESCRIPTION = pathlib.Path('README.rst').read_text('utf-8')

requires = {
    'install': [],
    'setup': [],
    'tests': ['flake8'],
    'sync': ['requests', 'websocket-client'],
    'aiohttp': ['aiohttp']
}

setuptools.setup(
    name='slack-sansio',
    long_description=LONG_DESCRIPTION,
    description='(a)sync Slack API library',
    keywords=[
        'bot',
        'slack',
        'api',
        'sans-io',
        'async'
    ],
    packages=setuptools.find_packages(),
    zip_safe=True,
    install_requires=requires['install'],
    setup_requires=requires['setup'],
    tests_require=requires['tests'],
    extras_require=requires,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    author='Ovv',
    author_email='contact@ovv.wtf',
    license='MIT',
    url='https://github.com/pyslackers/slack-sansio',
    version='0.1.0',
)
