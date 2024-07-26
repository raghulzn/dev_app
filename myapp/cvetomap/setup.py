from setuptools import setup

setup(
    name='cvetomap',
    version='1.0.0',
    packages=['cvetomap', 'cvetomap.nvd', 'cvetomap.open_ai'],
    url='https://linkedin.com/in/raghul-vijayakumar',
    license='MIT',
    author='Raghul V, Zeron',
    author_email= 'raghul1785@gmail.com',
    description='A tool to generate a complete analysis and threat report from vulnerabilities (CVE IDs) while '
                'perfectly complying with MITRE ATT&CK',
    install_requires=[
        'requests'
    ]
)
