import argparse


def set_arg_parser():
    parser = argparse.ArgumentParser(description='Process eeg data. See docs/main.txt for more info')
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="output verbosity")
    parser.add_argument("-d", "--driver", type=str, default='chrome',
                        help="Specify a specific webdriver")
    parser.add_argument("-c", "--challenge", type=int, choices=range(1,21), default=1,
                        help="Specify the challenge type (supporting facts) {1|2}")
    parser.add_argument("-a", "--arch", type=int, choices=[1, 2], default=1,
                        help="Specify the model archetecture (DMN, ConvLSTM) {1|2}")

    parser.add_argument("-b", "--batch_size", type=int, default=32,
                        help="Batch size for training")

    return parser