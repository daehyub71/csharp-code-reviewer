# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for C# Code Reviewer
Builds a single-file Windows executable with all resources bundled.
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

block_cipher = None

# Collect all resource files
resources_dir = os.path.join('resources', 'styles')
templates_dir = os.path.join('resources', 'templates')

added_files = [
    (resources_dir, 'resources/styles'),
    (templates_dir, 'resources/templates'),
]

# Collect PySide6 data files
pyside6_data = collect_data_files('PySide6')

# Hidden imports for PySide6
hidden_imports = collect_submodules('PySide6')
hidden_imports.extend([
    'markdown',
    'markdown.extensions.fenced_code',
    'markdown.extensions.codehilite',
    'markdown.extensions.tables',
    'Pygments',
    'Pygments.lexers.dotnet',
    'Pygments.formatters.html',
    'ollama',
    'matplotlib',
    'matplotlib.backends.backend_agg',
])

a = Analysis(
    ['app/main.py'],
    pathex=[],
    binaries=[],
    datas=added_files + pyside6_data,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib.tests',
        'numpy.tests',
        'PIL',
        'scipy',
        'pandas',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CodeReviewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # UPX compression for smaller EXE
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # TODO: Add icon file when available
)
