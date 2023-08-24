from setuptools import setup

setup(
    name='swmonkey',
    version='0.6',
    packages=['swmonkey'],
    author='Li Saifei',
    author_email='waltermitty121906@gmail.com',
    description='A tool for monkey test on Linux GUI',
    entry_points={
        'console_scripts': [
            'swmonkey = swmonkey.main:swmonkey'
        ]
    },
    install_requires=[
        'pyautogui',
        'psutil',
    ]
)