from setuptools import setup, find_packages

setup(
    name="mtcli-trade",
    version="1.2.0",
    description="Plugin mtcli para gerenciamento de ordens",
    author="Valmir França da Silva",
    author_email="vfranca3@gmail.com",
    packages=find_packages(include=["mtcli_trade", "mtcli_trade.*"]),
    install_requires=[
        "mtcli>=1.18.1,<2.0.0"
    ],
    entry_points={
        "mtcli.plugins": [
"mtcli-trade = mtcli_trade.trade:trade"
        ]
    },
)
