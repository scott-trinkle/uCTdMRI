from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='strtens',
      version='0.1',
      description='Tools for using synchrotron microCT images to validate diffusion MRI in whole mouse brains.',
      long_description=readme(),
      url='https://github.com/scott-trinkle/uCTdMRI',
      author='Scott Trinkle',
      author_email='tscott.trinkle@gmail.com',
      license='MIT',
      packages=['strtens'],
      install_requires=['numpy', 'scikit-image', 'scipy', 'tifffile'],
      zip_safe=False)