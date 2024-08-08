from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="FeynmanAi",
    version="0.1.2",
    description="A command-line tool for using RAG model on Local documents",
    long_description=long_description,
    long_description_content_type="text/markdown",


    author="Oscar Karuga N",
    author_email="oscarkaruga1@gmail.com",
    url="https://github.com/oscar066/FeynmanAI.git",

    packages=find_packages(exclude=["tests", "**pycache"]),

    install_requires = [
        "haystack-ai",
        "datasets>=2.6.1",
        "sentence-transformers>=2.2.0",
        "python-dotenv", 
        "pypdf",
        "python-docx",
        "python-pptx",
        "colorlog",
        "colorama",
    ],

    entry_points={
        "console_scripts" : [
            "FeynmanAi=rag_cli:main"
        ]
    },

    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)