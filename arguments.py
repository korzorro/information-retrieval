from argparse import ArgumentParser

PROG_NAME = 'IR'

OPTS = (
    ('-b', {'help': 'Binary Retrieval',
            'action': 'store_true'}),
)


def get_arguments():
    parser = setup_argument_parser()
    return parser.parse_args()


def setup_argument_parser():
    parser = ArgumentParser(prog=PROG_NAME)
    for key, val in OPTS:
        parser.add_argument(key, **val)
    return parser
