import pathlib

import setuptools

LONG_DESCRIPTION = pathlib.Path("README.rst").read_text("utf-8")

requires = {
    "requests": ["requests", "websocket-client"],
    "aiohttp": ["aiohttp"],
    "curio": ["curio", "asks"],
    "trio": ["trio", "asks"],
    "treq": ["treq"],
    "all": set(),
    "doc": ["sphinx", "sphinxcontrib-asyncio", "sphinxcontrib-napoleon"],
    "install": [],
}
requires["all"].update(
    requires["install"],
    requires["requests"],
    requires["aiohttp"],
    requires["curio"],
    requires["trio"],
    requires["treq"],
)


def find_version():
    with open("slack/__version__.py") as f:
        version = f.readlines()[-1].split("=")[-1].strip().strip("'").strip('"')
        if not version:
            raise RuntimeError("No version found")

    return version


setuptools.setup(
    name="slack-sansio",
    long_description=LONG_DESCRIPTION,
    description="(a)sync Slack API library",
    keywords=["bot", "slack", "api", "sans-io", "async"],
    packages=setuptools.find_packages(),
    install_requires=requires["install"],
    extras_require=requires,
    # python_requires='>=3.6',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    author="Ovv",
    author_email="contact@ovv.wtf",
    license="MIT",
    url="https://github.com/pyslackers/slack-sansio",
    version=find_version(),
    include_package_data=True,
    package_data={"slack": ["py.typed"]},
)
