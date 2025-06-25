from setuptools import setup

setup(
    name='PokerTimerApp',
    version='1.0',
    packages=[''],
    package_data={'': ['config.yaml', 'icon.png']},
    include_package_data=True,
    install_requires=[
        # List your dependencies here, e.g., 'tkinter'
    ],
    entry_points={
        'gui_scripts': [
            'poker-timer = main:run',  # Changed to point to main.py's run function
        ],
    },
)
