#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="glm-codelens",
    version="1.0.0",
    author="GitHub Developer",
    author_email="developer@example.com",
    description="🪞 GLM-CodeLens - 基于GLM-5.1的智能代码分析引擎",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/GLM-CodeLens",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "glm": ["requests>=2.28.0"],
    },
    entry_points={
        "console_scripts": [
            "glm-codelens=src.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
