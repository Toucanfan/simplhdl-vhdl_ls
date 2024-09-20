from setuptools import setup, find_packages
#from src.importlistparser import __version__


setup(
    name='SimplHDL-vhdl_ls',
    description='Generate VHDL_LS configuration from SimplHDL project.',
    version=0.1,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'simplhdl.plugins': [
            'flow=vhdl_ls'],
    },
    install_requires=[
        'SimplHDL',
        'Jinja2'
    ],
)
