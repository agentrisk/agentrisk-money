from setuptools import setup, find_packages

setup(
    name="money",
    version="1.0.0",
    description="Python lib for dealing with Money without floating point errors",
    long_description="Python class for working with money, following Martin Fowler's money pattern.",
    author="AgentRisk",
    author_email="hello@agentrisk.com",
    license="MIT",
    packages=find_packages(
        exclude=["test", ".gitignore", "README.md", ".tool-versions", ".vscode", "venv"]),
    install_requires=["Babel>=2.8.0"],
    url="https://github.com/agentrisk/agentrisk-money",
    classifiers=[],
)
