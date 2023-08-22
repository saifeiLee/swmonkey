from setuptools import setup

setup(
    name='sw-monkey',
    version='0.1',
    packages=['src'],
    author='Li Saifei',
    author_email='waltermitty121906@gmail.com',
    description='A tool for monkey test on Linux GUI',
    install_requires=[
        'pyautogui',
        'psutil',

    ]
)