from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="postnl_api",
    version="1.2.2",
    description="Python wrapper for the PostNL API, a way to track packages and letters.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imicknl/python-postnl-api",
    author="Mick Vleeshouwer",
    author_email="mick@imick.nl",
    license="MIT",
    install_requires=["requests>=2.0"],
    packages=find_packages(),
    zip_safe=True,
)
