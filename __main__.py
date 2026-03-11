import os,sys
from avamp.core.logging    import LOG
from avamp.core.dispatcher import VisualDispatcher
from avamp.core         import parsers
from avamp.ui           import app

import argparse


def make_test_data():
    try:
        TEST_DATA = os.path.join(os.path.dirname(__file__), "testdata", "test_data.csv")
        if(not os.path.exists(TEST_DATA)):
            LOG.info("Test data not found, generating test data...")
            LOG.info(f"Running: '{sys.executable} testdata{os.path.sep}make_test_data.py'")
            print("")
            print("Generation ...")
            print("")
            os.system(f"{sys.executable} testdata{os.path.sep}make_test_data.py")
            print("")
    except Exception as e:
        LOG.error(f"Error generating test data: {e}")
        sys.exit(1)

# User argumets
def create_user_parser():
    parser = argparse.ArgumentParser(description="AVAMP Application")
    parser.add_argument(
        "-C", "--path", type=str, default="." ,help="Root path for file browser"
    )
    parser.add_argument(
        "-T", "--test", action="store_true", help="Run in test mode with test data"
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
    # Generate test data if not present
    if(args.test): make_test_data()
    app.main(os.path.abspath(args.path))
