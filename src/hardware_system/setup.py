from setuptools import find_packages, setup

package_name = 'hardware_system'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/hardware_system.launch.py']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jacinto',
    maintainer_email='jose.jacinto7129@alumnos.udg.mx',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'operador = hardware_system.operador:main',
            'monitor = hardware_system.monitor:main',
            'emulador = hardware_system.emulador:main',
        ],
    },
)
