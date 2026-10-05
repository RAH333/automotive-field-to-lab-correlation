import numpy as np
import pandas as pd
from scipy import signal

def clean_telemetry_data(filepath: str) -> pd.DataFrame:
    """Loads and filters high-frequency field strain/acceleration data."""
    df = pd.read_csv(filepath)
    
    # Low-pass filter to remove high-frequency sensor noise (>100 Hz)
    fs = 1000  # Sampling rate 1000Hz
    nyq = 0.5 * fs
    cutoff_ratio = 100 / nyq
    b, a = signal.butter(4, cutoff_ratio, btype='low')
    
    for col in df.select_dtypes(include=[np.number]).columns:
        if col != 'time':
            df[col] = signal.filtfilt(b, a, df[col])
            
    return df

def generate_mock_field_data():
    """Generates synthetic tractor field telemetry for demonstration."""
    t = np.linspace(0, 10, 10000)
    # Simulate steady load + high impact structural bumps
    base_strain = 150 * np.sin(2 * np.pi * 5 * t) 
    shocks = np.random.normal(0, 30, len(t))
    shocks[5000:5100] += 500  # Simulate a severe structural field impact
    
    df = pd.DataFrame({
        'time': t,
        'strain_microstrain': base_strain + shocks
    })
    df.to_csv('data/raw_field_telemetry.csv', index=False)
  
