import argparse
from services.death_finder import DeathFinder

parser = argparse.ArgumentParser(
    prog="Death Finder",
    description="Bulk Scraper for Framingham and LIN Calculator"
)

parser.add_argument("csv", help="Path to the csv containing the diagnostics")
parser.add_argument(
    "output",
    nargs="?",
    default=".",
    help="Path to the output file or folder (default: current directory)"
)

parser.add_argument("-d", "--debug", action="store_true", help="Enables debug mode")

calculator_group = parser.add_mutually_exclusive_group(required=True)
calculator_group.add_argument("-f", "--framingham", action="store_true", help="Uses only the Framingham calculator")
calculator_group.add_argument("-l", "--lin", action="store_true", help="Uses only the LIN calculator")

args = parser.parse_args()

death_finder = DeathFinder(args)
death_finder.calculate()
