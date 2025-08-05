import os,sys
from avamp.core.logging    import LOG
from avamp.core.dispatcher import VisualDispatcher
from avamp.core         import parsers
from avamp.ui           import app

import argparse

# Generate test data if not present
TEST_DATA = os.path.join(os.path.dirname(__file__), "testdata", "test_data.csv")
if(not os.path.exists(TEST_DATA)):
    LOG.info("Test data not found, generating test data...")
    LOG.info(f"Running: '{sys.executable} testdata{os.path.sep}make_test_data.py'")
    print("")
    print("Generation ...")
    print("")
    os.system(f"{sys.executable} testdata{os.path.sep}make_test_data.py")
    print("")

# User argumets
def create_user_parser():
    parser = argparse.ArgumentParser(description="AVAMP Application")
    parser.add_argument(
        "-C", "--path", type=str, default="." ,help="Root path for file browser"
    )
    return parser

# Getter for user arguments
def parse_args():
    parser = create_user_parser()
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    LOG.info("Vamp Init")
    args = parse_args()
    app.main(os.path.abspath(args.path))
