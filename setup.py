from setuptools import setup, find_packages

setup(
    name="qbot",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "ollama>=0.3.3",
        "chromadb>=0.4.22",
        "flask>=2.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
        ],
    },
    author="Your Name",
    description="Q&A bot using Ollama with vector store",
    python_requires=">=3.8",
)
