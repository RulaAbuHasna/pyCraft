from setuptools import setup, find_packages

setup(
    name='pyCraft',  # Updated package name
    version='0.1.0',
    packages=find_packages(),
    install_requires=[  # Optional dependencies can go here, like any libraries you're using
        'typing',  # Include typing if you're using type hints in older versions of Python
    ],
    author='Rola Abuhasna',
    author_email='rula.abuhasna@gmail.com',  # Optional
    description='A versatile package providing custom functionalities for developers.',
    long_description=open('README.md').read(),  # Ensure you have a README.md for more detailed information
    long_description_content_type='text/markdown',
    url='https://github.com/RulaAbuhasna/pyCraft',  # Update with your actual repository URL
    classifiers=[  # Optional, for adding more context about the package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Specify the Python version compatibility
)
