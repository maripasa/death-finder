import argparse
from services.death_finder import DeathFinder

parser = argparse.ArgumentParser(
    prog="Death Finder",
    description="Bulk Scraper for Framingham and LIN Calculator"
)

parser.add_argument("-d", "--debug", action="store_true", help="Enables debug mode")
parser.add_argument(
    "--wait",
    type=float,
    default=0.5,
    help="Wait time in seconds"
)

subparsers = parser.add_subparsers(dest="calculator", required=True)

framingham_parser = subparsers.add_parser("framingham", help="Run the Framingham calculator")
framingham_parser.add_argument(
    "csv",
    nargs="?",
    default=".",
    help="Path to the csv containing the diagnostics"
)
framingham_parser.add_argument(
    "output",
    nargs="?",
    default=".",
    help="Path to the output file or folder"
)

lin_parser = subparsers.add_parser("lin", help="Run the LIN calculator")
lin_parser.add_argument(
    "csv",
    nargs="?",
    default=".",
    help="Path to the csv containing the diagnostics"
)
lin_parser.add_argument(
    "output",
    nargs="?",
    default=".",
    help="Path to the output file or folder"
)

args = parser.parse_args()

death_finder = DeathFinder(args)
death_finder.calculate()
