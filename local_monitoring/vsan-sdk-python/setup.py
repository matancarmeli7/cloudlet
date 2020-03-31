import re
import ast

from setuptools import setup, find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('src/vmware/vsan/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1))
    )

setup(
    name='pyvsan',
    version=version,
    description='VMware vSAN SDK for Python',
    long_description=open('README.md').read(),
    author='VMware, Inc.',
    author_email='unknown@vmware.com',
    maintainer='John Doe',
    maintainer_email='john.doe@example.org',
    license='BSD',
    url='https://code.vmware.com/apis/398/vsan',
    download_url='https://code.vmware.com/apis/398/vsan',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    project_urls={
        'Documentation': 'https://code.vmware.com/apis/398/vsan',
        'Download': 'https://code.vmware.com/web/sdk/6.7.0/vsan-python',
    },
    scripts=[
        'src/vsanapisamples',
        'src/vsaniscsisamples',
    ],
    install_requires=[
        'pyvmomi >= 6.7.0',
    ]
)

