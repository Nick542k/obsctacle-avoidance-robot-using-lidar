from setuptools import setup, find_packages
from glob import glob
import os

package_name='mobile_robot'

setup(
    name=package_name,
    version='0.0.0',

    packages=find_packages(
        exclude=['test']
    ),

    data_files=[

        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),

        (
            'share/' + package_name,
            ['package.xml']
        ),

        (
            os.path.join(
                'share',
                package_name,
                'launch'
            ),

            glob('launch/*')
        ),

        (
            os.path.join(
                'share',
                package_name,
                'model'
            ),

            glob('model/*')
        ),

        (
            os.path.join(
                'share',
                package_name,
                'parameters'
            ),

            glob('parameters/*')
        ),

    ],

    install_requires=[
        'setuptools'
    ],

    zip_safe=True,

    maintainer='ahaber',

    maintainer_email='ahaber@todo.todo',

    description='Mobile robot package',

    license='Apache-2.0',

    tests_require=[
        'pytest'
    ],

    entry_points={
        'console_scripts': [
        'controller_final = mobile_robot.controller_final:main',

        ],
    },

)
