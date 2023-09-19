import os
from pathlib import Path
from collections import defaultdict

MAX_COPIES_RESERVED = 5

def delete_old_packages(directory):
    helmpath = Path(directory)
    helmpackages = list(helmpath.glob("*.tgz"))

    package_versions = defaultdict(list)
    for package in helmpackages:
        package_name = package.name.rsplit(".", 2)[0]
        package_versions[package_name].append(package)

    packages_to_delete = [pkg for pfiles in package_versions.values() for pkg in sorted(pfiles, key=lambda x: x.name.split('.')[-2], reverse=True)[MAX_COPIES_RESERVED:]]

    for ptd in packages_to_delete:
        os.remove(ptd)

def process_repositories():
    delete_old_packages("snapshot/packages")

if __name__ == "__main__":
    process_repositories()
