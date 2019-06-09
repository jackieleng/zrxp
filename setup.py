from setuptools import setup, find_packages

setup(
    name="zrxp",
    version="0.1.0",
    author="Jackie Leng",
    packages=find_packages(),
    url="https://github.com/jackieleng/zrxp",
    license="LICENSE.txt",
    description="ZRXP",
    long_description=open("README.md").read(),
    install_requires=["pandas", "parsimonious"],
)
