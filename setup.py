import pathlib
import setuptools

LONG_DESCRIPTION = pathlib.Path('README.rst').read_text('utf-8')

requires = {
    'install': [],
    'setup': ['pytest-runner'],
    'tests': ['flake8', 'pytest>=3.3.0', 'coverage', 'pytest-coverage', 'pytest-asyncio', 'asynctest'],
    'full': set(),
    'doc': {'sphinx', 'sphinxcontrib-asyncio', 'sphinxcontrib-napoleon'},
    'dev': {'tox'},
    'requests': ['requests', 'websocket-client'],
    'aiohttp': ['aiohttp'],
    'curio': ['curio', 'asks'],
    'trio': ['trio', 'asks'],
    'treq': ['treq'],
}

requires['dev'].update(*requires.values())
requires['doc'].update(requires['tests'])
requires['full'].update(requires['requests'], requires['aiohttp'], requires['curio'], requires['trio'],
                        requires['treq'])


def find_version():
    with open("slack/__version__.py") as f:
        version = f.readlines()[-1].split('=')[-1].strip().strip("'").strip('"')
        if not version:
            raise RuntimeError('No version found')

    return version


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
    # python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
    ],
    author='Ovv',
    author_email='contact@ovv.wtf',
    license='MIT',
    url='https://github.com/pyslackers/slack-sansio',
    version=find_version(),
)
