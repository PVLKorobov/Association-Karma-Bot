from distutils.core import setup
import py2exe


setup(console=['main.py'], py_modules=['tools, set_commands'], options={'py2exe':{'packages':['charset_normalizer']}}, name='TG Karma Bot', version='1.0')