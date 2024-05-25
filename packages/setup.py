from setuptools import setup, find_packages

# To create the package:
# 1: Use 'pip install build' in this root folder.
# 2: Go to packages folder and use 'python -m build'.

# To install the project:
# 1: Go to dist folder and use 'pip install api_catastro-0.1-py3-none-any.whl --force-reinstall'.

setup(
    name='api_catastro',
    version='0.1',
    description='Obtener los datos del catastro para una referencia catastral usando su API oficial.',
    author='Luis Cerdeño Mota',
    author_email='luiscerdenomota@gmail.com',
    packages=find_packages(),
    install_requires=['pandas', 'requests', 'tqdm', 'openpyxl']
)
