import sys, pathlib

# Add the project root to sys.path so tests can import the 'etl' package.
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
