import os

from setuptools import find_packages, setup

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, "README.MD"), encoding="utf-8") as f:
    long_description = "".join(f.readlines())

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setup(
    name="dna_analyser_ibp",
    version=version,
    description="DNA analyser API wrapper tool for Jupiter notebooks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Patrik Kaura",
    author_email="patrikkaura@gmail.com",
    keywords="dna, ibp, quadruplex, g4hunter, g4killer, palindrome, p53, analysis",
    license="GPLv3",
    url="https://gitlab.com/PatrikKaura/DNA_analyser_IBP/",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
        "tqdm",
        "pyjwt",
        "matplotlib",
        "requests-toolbelt",
        "tenacity",
    ],
    classifiers=[
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    zip_safe=False,
)
