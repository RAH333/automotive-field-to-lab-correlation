import numpy as np
import pandas as pd

def simple_rainflow_damage(stress_history: np.ndarray) -> float:
    """
    Simplified damage estimation using a basic peak-valley counter 
    and Miner's Rule for cumulative fatigue damage analysis.
    """
    # Extract local extrema (peaks and valleys)
    dx = np.diff(stress_history)
    extrema = stress_history[1:][dx[:-1] * dx[1:] < 0]
    
    if len(extrema) < 2:
        return 0.0
        
    # Calculate simple peak-to-valley ranges
    ranges = np.abs(np.diff(extrema))
    
    # Material constant properties (Basquin's exponent for steel)
    m = 5
    C = 1e18 
    
    # Cumulative Damage accumulation (Miner's Rule: Sum(n_i / N_i))
    total_damage = np.sum((ranges ** m) / C)
    return float(total_damage)

def evaluate_correlation(field_path: str, lab_path: str) -> dict:
    """Correlates damage signatures between field conditions and lab rig profiles."""
    field_df = pd.read_csv(field_path)
    lab_df = pd.read_csv(lab_path)
    
    field_damage = simple_rainflow_damage(field_df['strain_microstrain'].values)
    # Lab rig scales up amplitude to compress validation testing time
    lab_damage = simple_rainflow_damage(lab_df['rig_strain_microstrain'].values)
    
    # Target lab acceleration factor (e.g., 1 hour lab = 10 hours field)
    correlation_ratio = lab_damage / (field_damage + 1e-9)
    
    return {
        "field_damage_index": field_damage,
        "lab_damage_index": lab_damage,
        "acceleration_factor": correlation_ratio,
        "status": "PASS" if 8.0 <= correlation_ratio <= 12.0 else "RE-CALIBRATE RIG"
    }

def generate_mock_lab_data():
    """Generates synthetic accelerated laboratory rig profile data."""
    t = np.linspace(0, 1, 1000) # Compressed time
    # Lab rig runs at higher frequency and optimized amplitudes
    rig_strain = 450 * np.sin(2 * np.pi * 25 * t)
    df = pd.DataFrame({
        'time': t,
        'rig_strain_microstrain': rig_strain
    })
    df.to_csv('data/lab_rig_profile.csv', index=False)
  
