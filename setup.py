from setuptools import setup, find_packages

setup(
    name='mousecontroller',
    version='1.0.4',
    author='Freddie Rayner',
    author_email='freddie.rayner.w@gmail.com',
    packages=find_packages(),
    url='https://pypi.org/project/mousecontroller/',
    license='LICENSE',
    description='A python package to easily control the mouse in realistic and fluent ways.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    scripts=['mousecontroller.py'],
    install_requires=['pypiwin32', 'keyboard'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
