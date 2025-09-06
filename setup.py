from setuptools import setup, find_packages

setup(
    name="mtcli-trade",
    version="1.2.0",
    description="Plugin mtcli para gerenciamento de órdens e posições",
    author="Valmir França da Silva",
    author_email="vfranca3@gmail.com",
    packages=find_packages(),
    install_requires=[
        "mtcli>=1.19.4,<2.0.0",
    ],
    entry_points={
        "mtcli.plugins": [
            "trade = mtcli_trade.trade:trade",
        ],
    },
    python_requires='>=3.10,<3.14',
)
