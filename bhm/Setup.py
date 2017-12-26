from setuptools import setup
from bhm import __init__

setup(name='bhm',
      version=__init__.__version__,
      author=__init__.__author__,
      author_email=__init__.__email__,
      description='Convert Korean down talk to honorific talk',
      install_requires=[
          "hgtk"
      ])