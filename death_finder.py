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

parser.add_argument(
    "calculator",
    choices=["framingham", "lin"],
    help="Type of calculator to run (framingham or lin)"
)

parser.add_argument(
    "csv",
    help="Path to the CSV containing the diagnostics"
)

parser.add_argument(
    "output",
    nargs="?",
    default=".",
    help="Path to the output file or folder (defaults to current directory)"
)

args = parser.parse_args()

death_finder = DeathFinder(args)
death_finder.calculate()
