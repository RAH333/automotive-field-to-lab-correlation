import numpy as np
from src.fatigue_analysis import simple_rainflow_damage

def test_zero_damage_on_flat_signal():
    flat_signal = np.ones(100) * 100
    damage = simple_rainflow_damage(flat_signal)
    assert damage == 0.0

def test_damage_increases_with_amplitude():
    low_signal = np.array([10, -10, 10, -10])
    high_signal = np.array([100, -100, 100, -100])
    
    assert simple_rainflow_damage(high_signal) > simple_rainflow_damage(low_signal)
