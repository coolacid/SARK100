"""
bands.py
Defines amateur radio bands and provides frequency generation utilities.
"""

bands = {
    "160m": {'start': 1800000, 'end': 2000000},
    "80m": {'start': 3500000, 'end': 4000000},
    "60m": {'start': 5300000, 'end': 5500000},
    "40m": {'start': 7000000, 'end': 7300000},
    "30m": {'start': 10100000, 'end': 10150000},
    "20m": {'start': 14000000, 'end': 14350000},
    "17m": {'start': 18060000, 'end': 18168000},
    "15m": {'start': 21000000, 'end': 21450000},
    "12m": {'start': 24890000, 'end': 24990000},
    "10m": {'start': 28000000, 'end': 29700000},
    "6m": {'start': 50000000, 'end': 54000000},
    "hf": {'start': 1800000, 'end': 30000000},
}


def generate_band_frequencies(band_name: str, buffer_pct: float = 0.0, step_hz: int = 1000):
    """
    Generate frequencies for a named ham band with optional buffer before and after,
    rounding start and end to the nearest kHz.

    Parameters
    ----------
    band_name : str
        Name of the band, e.g. "20m"
    buffer_pct : float
        Percentage of the band width to add before and after the band
        e.g., 0.1 adds 10% of the band width before start and after end
    step_hz : int
        Frequency step in Hz between consecutive values

    Returns
    -------
    List[int]
        List of frequencies including buffer, from start to end with given step

    Raises
    ------
    ValueError
        If the band_name is not found in the global bands dictionary
    """
    if band_name not in bands:
        raise ValueError(f"Band '{band_name}' not found in the bands dictionary.")

    band = bands[band_name]
    start = band["start"]
    end = band["end"]

    if start == end:
        # Single-frequency allocation, round to nearest kHz
        return [round(start / 1000) * 1000]

    band_width = end - start
    buffer = band_width * buffer_pct

    # Apply buffer and round to nearest kHz
    buffered_start = max(0, int((start - buffer) // 1000 * 1000))  # floor to nearest kHz
    buffered_end = int(((end + buffer + 999) // 1000) * 1000)       # ceil to nearest kHz

    frequencies = list(range(buffered_start, buffered_end + 1, step_hz))
    return frequencies
