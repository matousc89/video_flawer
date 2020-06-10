from distutils.core import setup
setup(
  name = 'video_flawer',
  packages = ['video_flawer'],
  version = '0.0.1',
  license='MIT',
  description = 'This package enhances video files with artifical defects.',
  author = 'Matous Cejnek, Yang Hong-Bin',
  author_email = 'matousc@gmail.com',
  url = 'https://github.com/matousc89/video_flawer',
  download_url = 'https://github.com/matousc89/video_flawer/archive/v_01.tar.gz',# TODO
  keywords = ['video', 'noise', 'artificial'],
  install_requires = [
          'numpy',
          'opencv-python',
      ],
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)