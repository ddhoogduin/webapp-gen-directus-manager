import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="wg-directus-manager",
    version="0.0.1",
    author="Dylan Hoogduin",
    author_email="ddhoogduin@gmail.com",
    description="This package provides command-line functions to"
                " manage directus projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddhoogduin/webapp-gen-directus-manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
