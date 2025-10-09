"""
Setup configuration for TopogenTech Satellite Embeddings Downloader library.
"""

from setuptools import setup, find_packages

# Read README for long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A modular library for downloading satellite embeddings from Google Earth Engine."

# Read requirements
try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
except FileNotFoundError:
    requirements = [
        "earthengine-api>=0.1.350",
        "google-cloud-storage>=2.0.0",
        "typing-extensions>=4.0.0",
    ]

setup(
    name="topogentech",
    version="0.1.0",
    author="TopogenTech Team",
    author_email="contact@topogentech.com",
    description="A modular library for downloading satellite embeddings from Google Earth Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DaVas1410/TopoGenTech",
    project_urls={
        "Bug Tracker": "https://github.com/DaVas1410/TopoGenTech/issues",
        "Documentation": "https://github.com/DaVas1410/TopoGenTech/blob/main/README.md",
        "Source Code": "https://github.com/DaVas1410/TopoGenTech",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "topogentech-download=topogentech.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "topogentech": ["py.typed"],
    },
    keywords=[
        "satellite",
        "embeddings", 
        "google-earth-engine",
        "remote-sensing",
        "geospatial",
        "machine-learning",
        "topological-data-analysis",
        "palm-oil",
        "deforestation",
        "ecuador",
    ],
    zip_safe=False,
)