# Death Finder

A bulk scraper for calculating Framingham and LIN risk scores using Selenium. This tool processes diagnostic data from a CSV file and outputs the results in JSON format.

---

## Features
- **Framingham Calculator**: Calculates 10-year risk of myocardial infarction (MI) or death.
- **LIN Calculator**: (To be implemented).
- **Output**: Results are saved in JSON format, with support for missing or invalid data.

---

## Usage

```bash
usage: Death Finder [-h] [-d] [--wait WAIT] {framingham,lin} csv [output]

Bulk Scraper for Framingham and LIN Calculator

positional arguments:
  {framingham,lin}  Type of calculator to run (framingham or lin)
  csv               Path to the CSV containing the diagnostics
  output            Path to the output file or folder (defaults to current directory)

options:
  -h, --help        Show this help message and exit
  -d, --debug       Enable debug mode
  --wait WAIT       Wait time in seconds (default: 0.5)
