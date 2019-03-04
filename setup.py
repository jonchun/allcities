import setuptools
import allcities

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='allcities',
    version=allcities.__version__,
    author=allcities.__author__,
    author_email=allcities.__author_email__,
    description=allcities.__doc__.strip(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Jonchun/allcities',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    package_data={
        'allcities': ['data/*'],
    },
    license='MIT',
)
