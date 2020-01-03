import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="integraty",
    version="0.0.1",
    author="Sam",
    author_email="szaydel@corelight.com",
    description="Integration testing library subclassing Pythons own unittest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://internal",
    packages=setuptools.find_packages(),
    install_requires=[
        "delegator.py>=0.1.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
