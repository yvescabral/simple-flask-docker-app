from setuptools import find_packages
from setuptools import setup

with open("README.md", encoding="utf8") as f:
    readme = f.read()

setup(
    name="testing_app",
    version="1.0.0",
    url="https://flask.palletsprojects.com/tutorial/",
    description="The basic app.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
    extras_require={"test": ["pytest", "coverage"]},
)
