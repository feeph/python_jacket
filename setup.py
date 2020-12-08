import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jacket-feeph",
    version="0.1.0",
    author="Feeph Aifeimei",
    author_email="Chophuquie@outlook.com",
    description="wraps your application for CLI, AWS Lambda or Flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/feeph/python_jacket",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
