import os
from pathlib import Path
from collections import defaultdict

MAX_COPIES_RESERVED = 5

def delete_old_packages(directory):
    helmpath = Path(directory)
    helmpackages = list(helmpath.glob("*.tgz"))

    version_modifiers = {'rc': 1, 'snapshot': 2}

    def get_version_num(file):
        version_part = file.name.rsplit("-", 2)[-1].split('.')[:-1]
        if 'rc' in map(str.lower, version_part):
            return None
        return [int(num) if num.isdigit() else version_modifiers.get(num.lower(), 999) for num in version_part]

    package_versions = defaultdict(list)
    for package in helmpackages:
        package_name = '-'.join(package.name.rsplit("-", 2)[:-1])
        if get_version_num(package) is not None:
            package_versions[package_name].append(package)

    packages_to_delete = [pkg for pfiles in package_versions.values() for pkg in sorted(pfiles, key=get_version_num, reverse=True)[MAX_COPIES_RESERVED:]]

    for ptd in packages_to_delete:
        os.remove(ptd)

def process_repositories():
    delete_old_packages("snapshot/packages")

if __name__ == "__main__":
    process_repositories()
