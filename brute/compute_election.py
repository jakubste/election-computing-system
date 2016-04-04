#!/usr/bin/env python

import sys

from ecs.application import ElectionComputingSystem

if __name__ == "__main__":
    argv = sys.argv

    if len(argv) != 4:
        print "Usage: python {} <p_parameter> <file_name> <committee_size>".format(argv[0])
        exit()

    app = ElectionComputingSystem(argv[1], argv[3])
    app.load_data_from_file(argv[2])
    app.run()
