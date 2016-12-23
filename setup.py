from setuptools import setup

setup(
    name='spotiphile',
    version='0.0.1-dev',
    description='Download music from Spotify',
    packages=['spotiphile', ],
    scripts=['bin/spotiphile'],
    install_requires=[
        'requests', 'youtube_dl', 'google-api-python-client', 'mutagen'
    ],
    license='MIT'
    # long_description=open('README.md').read(),
)
