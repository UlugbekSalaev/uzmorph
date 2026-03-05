from setuptools import setup, find_packages

setup(
    name="uzmorph",
    version="0.1.0",
    author="Ulugbek Salaev",
    author_email="ulugbek.salaev@urdu.uz",
    description="A rule-based morphological analyzer for the Uzbek language based on CSE (Complete Set of Endings) and annotated morphological tags",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/UlugbekSalaev/uzmorph", 
    packages=find_packages(),
    py_modules=["uzmorph"],
    include_package_data=True,
    package_data={
        "": ["*.csv"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires='>=3.6',
    install_requires=[],
)
