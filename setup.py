from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine-tuning.
include_files = ['icon.ico', 'GitHub_Logo_small.png', 'config.ini']
build_options = {'packages': [], 'excludes': [], 'include_files': include_files}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('dcm-get.py', base=base, target_name='PACS_del_req_1.4')
]

setup(name='Deletion Request',
      version='1.5',
      description='Sends an image deletion request to google sheets',
      options={'build_exe': build_options},
      executables=executables)

# python setup.py build