"""Console script for branesta."""

import argparse
from datetime import datetime
import branesta

def main():
    """Console script for branesta."""
    # Unique identifier for current analysis
    ver = datetime.now().strftime("%Y%m%d%H%M%S")

    # Parse user inputs
    parser = argparse.ArgumentParser(description="Arguments for analysis.")
    parser.add_argument("srcdir", default="./",
                        help="path to source directory with time-series")
    parser.add_argument("outdir", default="./",
                        help="path to out directory for results and logs")
    parser.add_argument('win_len', default=30, type=int,
                        help="number of time-frames in each snapshot")
    parser.add_argument('--subnetpath','-s',
                        help="path to csv file with subnetwork labels and ixs, optional")
    parser.add_argument('--tot_len','-l', type=int,
                        help="expected total number of time frames, optional")
    parser.add_argument('--tot_roi_num','-r', type=int,
                        help="expected total number of ROIs, optional")
    args = parser.parse_args()

    # Call analysis
    analyze(ver, **vars(args))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover