from setuptools import setup

setup(
    name='VEmulator-CLI',
    version='1.0',
    py_modules=['vemulator_cli'],
    install_requires=[
        'Click',
        'vemulator'
    ],
    entry_points='''
        [console_scripts]
        vemulator-cli=vemulator_cli:cli
    '''
)
