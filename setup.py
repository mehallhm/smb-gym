"""The setup script for installing the package."""
from setuptools import setup, find_packages

setup(
    name='smbgym',
    version='0.0.3',
    description='Super Mario Bros. for OpenAI Gym',
    keywords=' '.join([
        'OpenAI-Gym'
        'Super-Mario-Bros',
        'Reinforcement-Learning-Environment'
    ]),
    classifiers=[
        'Development Status :: 1 - Active Development',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: Free For Educational Use',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    url='https://github.com/Mike968/smb-gym',
    author='Michael Mehall',
    author_email='michaelhmehall@gmail.com',
    license='Proprietary',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    package_data={ 'smb-gym': ['bin/ap.jar', 'original/*.txt'] },
    install_requires=['py4j>=0.10.0', 'numpy>=1.20.0'],
    include_package_data=True
)