#!/bin/bash
basedir=$1
export files="README.md LICENSE Taskfile.yml docker-compose.test.yml setup.py .github/workflows/qa.yml .github/workflows/quality_check.yml .github/workflows/release.yml"
for f in $files; do
    echo "Processing $basedir/$f"
    sed -f .kickoff.sed -i $basedir/$f
done
