import pkg_resources
import sys


def check(spec):
    name, version = spec
    try:
        dist = pkg_resources.get_distribution(name)
    except pkg_resources.DistributionNotFound:
        return False

    package_version = dist.version.split(".")
    require_version = version.split(".")
    return package_version >= require_version


def main():
    if not check(sys.argv[1:]):
        sys.exit(1)

if __name__ == '__main__':
    main()