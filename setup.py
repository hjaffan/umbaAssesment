import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="umba_assessment_flask",
    version="0.0.1",
    url="http://flask.pocoo.org/docs/tutorial/",
    license="BSD",
    maintainer="Hilal Jaffan",
    maintainer_email="hilal.jaffan@jaffan.io",
    description="This app is an assessment to show usage of python and code quality.",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],
    extras_require={"test": ["pytest", "coverage"]},
)