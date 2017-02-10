# -*- mode: python -*-

block_cipher = None
# work-around a bug in hook-botocore
from PyInstaller.utils.hooks import is_module_satisfies
import PyInstaller.compat
PyInstaller.compat.is_module_satisfies = is_module_satisfies

a = Analysis(['main.py'],
             pathex=['.\\'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='AWS-SSL-Manager',
          debug=False,
          strip=False,
          upx=True,
          console=False)
