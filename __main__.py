import os,sys
from avamp.core.logging import LOG
from avamp.core         import parsers
from avamp.frontends.qt6 import app

import argparse

TEST_DATA = os.path.join(os.path.dirname(__file__), "testdata", "test_data.csv")
if(not os.path.exists(TEST_DATA)):
    LOG.info("Test data not found, generating test data...")
    LOG.info(f"Running: '{sys.executable} testdata{os.path.sep}make_test_data.py'")
    print("")
    print("Generation ...")
    print("")
    os.system(f"{sys.executable} testdata{os.path.sep}make_test_data.py")
    print("")


def create_user_parser():
    parser = argparse.ArgumentParser(description="VAMP Application")
    parser.add_argument(
        "-C", "--path", type=str, default="." ,help="Root path for file browser"
    )
    return parser

def parse_args():
    parser = create_user_parser()
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    LOG.info("Vamp Init")
    args = parse_args()
    app.main(os.path.abspath(args.path))


    # LOG.info(f"Vamp Parsers: {parsers.PARSERS}")
    # for parser in parsers.PARSERS:
    #     LOG.info(f"Parser: {parser['name']} - Extension: {parser['ext']} - Class: {parser['cls']}")
    #     parser_ext = parser['ext']
    #     for ext in parser_ext:
    #         LOG.info(f"Parser Extension: {ext}")
    #         if( ext == "csv"):
    #             LOG.info(f"Testing CSV Parser with file: {TEST_DATA}")
    #             csv_parser = parser['cls'](TEST_DATA)
    #             for key in csv_parser.keys():
    #                 LOG.info(f"Key: {key}")
    #                 data = csv_parser.data(key)
    #                 LOG.info(f"Data for {key}: {data}")
    #                 plt.plot(data.x, data.y, label=key)

    #             plt.xlabel("Time")
    #             plt.ylabel("Value")
    #             plt.title("CSV Data Plot")
    #             plt.legend()
    #             plt.show()