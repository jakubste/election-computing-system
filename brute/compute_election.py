import sys

from ecs.application import ElectionComputingSystem

if __name__ == "__main__":
    argv = sys.argv

    if len(argv) != 3:
        print "Usage: python {} <p_parameter> <file_name>".format(argv[0])

    app = ElectionComputingSystem(argv[1])
    app.load_data_from_file(argv[2])
