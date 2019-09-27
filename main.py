#!/usr/bin/env python


class DcOps(object):
    def __init__(self):
        self._version = "0.0.1"

    @property
    def version(self):
        return self._version


def main():
    dcops = DcOps()
    print(dcops.version)


if __name__ == "__main__":
    main()
