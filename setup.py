from setuptools import setup
from setuptools import find_packages

version = "1.0.0"

install_requires = [
    "certbot>=1.1.0",
    "setuptools",
    "bawuenet-domainctl @ git+https://github.com/bawuenet/domainctl"
]

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="certbot-dns-bawuenet",
    version=version,
    description="bawue.net DNS Authenticator plugin for Certbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bawuenet/certbot-dns-bawuenet",
    author="Andreas",
    author_email="andreas@bawue.net",
    license="GPL v3",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "certbot.plugins": [
            "dns-bawuenet = certbot_dns_bawuenet.dns_bawuenet:Authenticator"
        ]
    },
#    test_suite="certbot_dns_bawuenet",
)
