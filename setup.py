import py2exe

version = '2.x'
path = f'../../release/karma_bot/{version}/dist'
py2exe.freeze(console=[{'script': 'main.py'}], 
              options={'packages': ['tools', 'handlers', 'charset_normalizer'],
                       'dist_dir': path})