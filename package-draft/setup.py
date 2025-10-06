setup(
    name='mlcommon-benchmark',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Your Name',
    author_email='your.email@example.com',
    description='A benchmark toolkit for ML common tasks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mlcommon-benchmark',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache 2.0',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'analyse-benchmarks=mlcommon_benchmark.generate:main',
        ],
    },
)
