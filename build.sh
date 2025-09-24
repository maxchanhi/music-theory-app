#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies from packages.txt
apt-get update && apt-get install lilypond

# Install python dependencies
pip install -r requirements.txt