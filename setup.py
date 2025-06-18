from setuptools import setup, find_packages

setup(
    name="credit_scoring_system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'scikit-learn>=1.0.0',
        'tensorflow>=2.6.0',
        'matplotlib>=3.4.0',
        'seaborn>=0.11.0',
        'joblib>=1.0.0'
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Credit scoring system with deep learning",
    license="MIT",
    keywords="credit scoring deep learning",
)