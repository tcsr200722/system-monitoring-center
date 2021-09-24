#!/usr/bin/env python3
from setuptools import setup, find_packages, os

changelog = 'debian/changelog'
if os.path.exists(changelog):
    head = open(changelog).readline()
    try:
        version = head.split("(")[1].split(")")[0]
    except:
        print("debian/changelog format is wrong for get version")
        version = ""
    f = open('src/__version__', 'w')
    f.write(version)
    f.close()

data_files = [
    ("/usr/share/applications/", ["integration/tr.org.pardus.system-monitoring-center.desktop"]),
    ("/usr/share/locale/tr/LC_MESSAGES/", ["translations/tr/system-monitoring-center.mo"]),
    ("/usr/share/system-monitoring-center/src", ["src/"]),
    ("/usr/share/system-monitoring-center/ui", ["ui/"]),
    ("/usr/share/icons/hicolor/scalable/actions/", ["icons/actions/"]),
    ("/usr/share/icons/hicolor/scalable/apps/", ["icons/apps/"]),
    ("/usr/share/polkit-1/actions", ["integration/tr.org.pardus.pkexec.system-monitoring-center.policy"]),
    ("/usr/bin/", ["integration/system-monitoring-center"])
]

setup(
    name="System Monitoring Center",
    version=version,
    packages=find_packages(),
    scripts=["system-monitoring-center"],
    install_requires=["PyGObject"],
    data_files=data_files,
    author="Hakan Dündar",
    author_email="hakandundar34coding@gmail.com",
    description="Provides information about system performance and usage.",
    license="GPLv3",
    keywords="system monitor task manager center performance speed frequency cpu usage ram usage swap memory memory usage storage network usage download speed fps frame ratio processes users startup programs services environment variables shell variables os",
    url="https://kod.pardus.org.tr/Hakan/system-monitoring-center",
)