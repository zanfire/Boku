try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "Home automation server",
    "author": "Matteo Valdina",
    "url": "URL to get it at.",
    "download_url": "Where to download it.",
    "author_email": "zanfire@gmail.com",
    "version": "0.1",
    "install_requires": ["nose", "cherrypy", "paho-mqtt"],
    "packages": ["bokuserver"],
    "scripts": [],
    "name": "bokuserver"
}

setup(**config)
