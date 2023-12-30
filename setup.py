import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='game_randomizer',
    version='0.2',
    author='Mat Martell',
    author_email='dev@matazar.net',
    description='A simple GUI/CLI app for selecting a random game based ' +
                 'on a JSON file of games.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/matazar/game_randomizer',
    packages=['game_randomizer'],
    package_dir={'game_randomizer': 'src'},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    test_suite="tests",
    install_requires=[
        'pillow>=9.5.0',
    ],
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        "console_scripts": [
            "game_randomizer=game_randomizer.app:gui_app",
            "game_randomizer_cli=game_randomizer.app:cli_app",
        ],
    },
)
