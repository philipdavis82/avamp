added_files = [
    ('avamp/core/parsers/base_parser.py','avamp/core/parsers/'),
    ('avamp/core/parsers/json/parser_test_3d_scene.py','avamp/core/parsers/json/'),
    ('avamp/core/parsers/csv/parser_simple_csv.py','avamp/core/parsers/csv/'),
    ('avamp/core/parsers/__init__.py','avamp/core/parsers/'),
    ('avamp/core/interfaces/*.py','avamp/core/interfaces/'),
]

options = [
    # ('v', None, 'OPTION'),
    # ('W ignore', None, 'OPTION'),
]

a = Analysis(
    ['__main__.py'],
    datas = added_files,
    binaries=None,
    hiddenimports=[],
    hookspath=None,
    runtime_hooks=None,
    excludes=None
)

pyz = PYZ(a.pure)
# exe = EXE(
#     pyz,
#     a.scripts,
#     a.datas,
#     options,
#     ...
# )

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Avamp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# coll = COLLECT(...)
coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        name='Avamp',
    )

#               splash.binaries,     # <-- splash binaries
#               ...)