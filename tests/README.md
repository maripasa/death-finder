usage: Death Finder [-h] [-d] (-f | -l) csv [output]

Bulk Scraper for Framingham and LIN Calculator

positional arguments:
  csv               Path to the csv containing the diagnostics
  output            Path to the output file or folder (default: current
                    directory)

options:
  -h, --help        show this help message and exit
  -d, --debug       Enables debug mode
  -f, --framingham  Uses only the Framingham calculator
  -l, --lin         Uses only the LIN calculator

results from <1% are treated as 1%
valid result filtering functions are based on the site this is scrapping from
