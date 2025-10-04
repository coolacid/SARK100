#!/usr/bin/env python3
import argparse
import sys
from pysark100 import sark100, bands

def main():
    parser = argparse.ArgumentParser(
        description="SARK100 Antenna Analyzer CLI"
    )

    # ✅ Global arguments
    parser.add_argument(
        "--device",
        type=str,
        required=False,
        default="/dev/ttyUSB0",
        help="Serial device for SARK100 (default: /dev/ttyUSB0)"
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Display a progress bar during the scan"
    )
    parser.add_argument(
        "--show-r",
        action="store_true",
        default=False,
        help="Show R line in plots"
    )
    parser.add_argument(
        "--show-x",
        action="store_true",
        default=False,
        help="Show X line in plots"
    )
    parser.add_argument(
        "--show-z",
        action="store_true",
        default=False,
        help="Show Z line in plots"
    )
    parser.add_argument(
        "--show-bands",
        action="store_true",
        default=True,
        help="Show ham bands in plots"
    )
    parser.add_argument(
        "--plot",
        nargs="?",
        const="scan_plot.png",
        type=str,
        help="Save PNG plot (optional filename, default: scan_plot.png)"
    )
    parser.add_argument(
        "--plot-interactive",
        action="store_true",
        help="Show interactive Plotly chart after scan"
    )
    parser.add_argument(
        "--show_df",
        action="store_true",
        help="Print the resulting dataframe to console"
    )
    parser.add_argument(
        "--plot-pyqt",
        action="store_true",
        help="Show PyQtGraph chart after scan"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- scan ----
    scan_parser = subparsers.add_parser("scan", help="Perform a full sweep of given frequencies")
    scan_parser.add_argument("--start", type=int, required=True, help="Start frequency in Hz")
    scan_parser.add_argument("--end", type=int, required=True, help="End frequency in Hz")
    scan_parser.add_argument("--step", type=int, default=10000, help="Step size in Hz (default: 10 kHz)")

    # ---- scan_band ----
    scan_band_parser = subparsers.add_parser("scan_band", help="Scan a predefined amateur radio band")
    scan_band_parser.add_argument("band", type=str, choices=[b for b in bands.keys()], help="Ham band name (e.g. 40m, 20m, 10m)")
    scan_band_parser.add_argument("--buffer", type=float, default=0.01, help="Percentage buffer before/after band edges (default: 1%%)")
    scan_band_parser.add_argument("--step", type=int, default=10000, help="Step size in Hz (default: 10 kHz)")

    args = parser.parse_args()

    # ---- Validate plot options ----
    if not (args.plot or args.plot_interactive or args.plot_pyqt or args.show_df):
        print("Error: You must provide at least one of --show_df, --plot, --plot-interactive, or --plot-pyqt")
        sys.exit(1)

    # Plot options dictionary
    plot_opts = {
        "include_r": args.show_r,
        "include_x": args.show_x,
        "include_z": args.show_z,
        "show_bands": args.show_bands
    }

    s = sark100(port=args.device)

    # ---- scan ----
    if args.command == "scan":
        pass
    # ---- scan_band ----
    elif args.command == "scan_band":
        data = s.scan_band(args.band, buffer_pct=args.buffer, step=args.step, progress=args.progress)
        if args.plot is not None:
            filename = args.plot or f"{args.band}_plot.png"
            data.plot(filename=filename, **plot_opts)
        if args.plot_interactive:
            data.plot_interactive(**plot_opts)
        if args.plot_pyqt:
            data.plot_pyqtgraph(**plot_opts)
        if args.show_df:
            print(data.get_dataframe())

if __name__ == "__main__":
    main()
