import pytest

def test_imports():
    import pysark100
    from pysark100 import sark100, bands
    from pysark100.bands import generate_band_frequencies
    assert hasattr(pysark100, "__version__")


def test_band_functionality():
    from pysark100.bands import bands, generate_band_frequencies
    assert "20m" in bands
    assert "40m" in bands
    freqs = generate_band_frequencies("20m", buffer_pct=0.01, step_hz=10000)
    assert len(freqs) > 0
    assert all(isinstance(f, int) for f in freqs)


def test_data_collector():
    from pysark100.collector import Sark100Collector
    collector = Sark100Collector()
    collector.add_measurement(14200000, "1.5,50.0,25.0,55.9")
    df = collector.get_data()
    assert len(df) == 1
    assert df["freq"][0] == 14200000
    assert abs(df["swr"][0] - 1.5) < 0.001
