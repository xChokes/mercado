#!/usr/bin/env python3
"""
Setup.py para el Simulador de Mercado con Agentes IA Hiperrealistas

Este archivo define los requerimientos de Python y facilita la instalación
del proyecto con un control estricto de versiones.
"""

from setuptools import setup, find_packages

# Leer requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f 
                   if line.strip() and not line.startswith('#')]

setup(
    name="simulador-mercado-ia",
    version="3.0.0",
    description="Simulador de Mercado con Agentes IA Hiperrealistas",
    long_description="Sistema avanzado de simulación económica con agentes de inteligencia artificial, machine learning y sistemas bancarios realistas.",
    author="Proyecto Mercado IA",
    python_requires=">=3.8",  # Versión mínima requerida de Python
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    extras_require={
        'dev': [
            'flake8>=6.0.0',
            'mypy>=1.0.0',
            'black>=23.0.0',
        ],
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'mercado-sim=main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="economia simulacion inteligencia-artificial machine-learning",
)