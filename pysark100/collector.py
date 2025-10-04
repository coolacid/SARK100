from pysark100.bands import bands

import polars as pl
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np


class Sark100Collector:
    def __init__(self):
        # Initialize an empty Polars DataFrame with correct types
        self.df = pl.DataFrame(
            schema=[
                ("freq", pl.Int64),
                ("swr", pl.Float64),
                ("r", pl.Float64),
                ("x", pl.Float64),
                ("z", pl.Float64)
            ]
        )

    def add_measurement(self, freq, measurement_str):
        """
        Add a single measurement to the DataFrame.
        measurement_str should be in the format: "swr,r,x,z"
        """
        try:
            swr, r, x, z = map(float, measurement_str.split(","))
        except ValueError:
            raise ValueError("measurement_str must be in the format 'swr,r,x,z' with numeric values")

        new_row = {
            "freq": freq,
            "swr": swr,
            "r": r,
            "x": x,
            "z": z
        }
        self.df = self.df.vstack(pl.DataFrame([new_row], schema=self.df.schema))

    def get_data(self):
        # Return the current Polars DataFrame
        return self.df

    def plot(self, include_r=False, include_x=False, include_z=False, show_bands=True, filename="plot.png"):
        plt.figure(figsize=(12, 6))

        freq_mhz = self.df["freq"].to_numpy() / 1_000_000

        # Plot SWR
        plt.plot(freq_mhz, self.df["swr"].to_numpy(), label="SWR", color="blue")

        # Optional plots
        if include_r:
            plt.plot(freq_mhz, self.df["r"].to_numpy(), label="R", color="green")
        if include_x:
            plt.plot(freq_mhz, self.df["x"].to_numpy(), label="X", color="orange")
        if include_z:
            plt.plot(freq_mhz, self.df["z"].to_numpy(), label="Z", color="red")

        # Overlay ham bands
        if show_bands:
            min_freq = self.df["freq"].min()
            max_freq = self.df["freq"].max()

            for band_name, band_info in bands.items():
                if band_name == "hf":
                    continue  # Skip 'hf'

                band_start = band_info["start"]
                band_end = band_info["end"]

                # Only include bands that intersect with the data range
                if band_end < min_freq or band_start > max_freq:
                    continue

                start_mhz = band_start / 1_000_000
                end_mhz = band_end / 1_000_000
                mid_mhz = (start_mhz + end_mhz) / 2

                # Grey shaded band area
                plt.axvspan(start_mhz, end_mhz, color="grey", alpha=0.3)

                # Vertical dashed line at mid frequency
                plt.axvline(x=mid_mhz, color="black", linestyle="--", linewidth=1, alpha=0.6)

                # Band label above the shaded area
                plt.text(
                    mid_mhz,
                    plt.ylim()[1] * 0.95,
                    band_name,
                    ha="center",
                    va="top",
                    fontsize=8,
                    color="black"
                )

        plt.xlabel("Frequency (MHz)")
        plt.ylabel("SWR / Impedance")
        plt.title("SARK100 Measurement")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

    def plot_interactive(self, include_r=False, include_x=False, include_z=False, show_bands=True):
        """
        Display an interactive Plotly chart of SWR (always) and optionally R, X, Z.
        Optionally overlay ham bands as shaded regions with labels and center lines.
        """
        freq_mhz = self.df["freq"].to_numpy() / 1_000_000

        fig = go.Figure()

        # Always add SWR
        fig.add_trace(go.Scatter(
            x=freq_mhz,
            y=self.df["swr"].to_numpy(),
            mode="lines",
            name="SWR",
            line=dict(color="blue")
        ))

        # Optionally add R, X, Z
        if include_r:
            fig.add_trace(go.Scatter(
                x=freq_mhz,
                y=self.df["r"].to_numpy(),
                mode="lines",
                name="R",
                line=dict(color="green")
            ))
        if include_x:
            fig.add_trace(go.Scatter(
                x=freq_mhz,
                y=self.df["x"].to_numpy(),
                mode="lines",
                name="X",
                line=dict(color="orange")
            ))
        if include_z:
            fig.add_trace(go.Scatter(
                x=freq_mhz,
                y=self.df["z"].to_numpy(),
                mode="lines",
                name="Z",
                line=dict(color="red")
            ))

        # Overlay ham bands
        if show_bands:
            min_freq = self.df["freq"].min()
            max_freq = self.df["freq"].max()

            for band_name, band_info in bands.items():
                if band_name == "hf":
                    continue  # Skip 'hf'

                band_start = band_info["start"]
                band_end = band_info["end"]

                # Only include bands that intersect with the data range
                if band_end < min_freq or band_start > max_freq:
                    continue

                start_mhz = band_start / 1_000_000
                end_mhz = band_end / 1_000_000
                mid_mhz = (start_mhz + end_mhz) / 2

                # Grey shaded box
                fig.add_vrect(
                    x0=start_mhz,
                    x1=end_mhz,
                    fillcolor="lightgrey",
                    opacity=0.3,
                    line_width=0
                )

                # Label above the band
                fig.add_annotation(
                    x=mid_mhz,
                    y=1,
                    yref="paper",
                    showarrow=False,
                    text=band_name,
                    font=dict(size=10, color="black"),
                    yshift=10
                )

                # Vertical dashed line at band midpoint
                fig.add_vline(
                    x=mid_mhz,
                    line=dict(color="black", width=1, dash="dash"),
                    opacity=0.6
                )

        # Layout
        fig.update_layout(
            title="SARK100 Measurement (Interactive)",
            xaxis_title="Frequency (MHz)",
            yaxis_title="SWR / Impedance",
            template="plotly_white"
        )

        fig.show()
