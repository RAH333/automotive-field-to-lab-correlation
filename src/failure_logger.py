import json
import pandas as pd

class DfmeaManager:
    """Manages failure modes, RPN calculation, and root-cause field actions."""
    def __init__(self, config_path: str):
        with open(config_path, 'file') as f:
            self.config = json.load(f)
        self.failure_log = []

    def log_failure_mode(self, mechanism: str, severity: int, occurrence: int, detection: int):
        """Calculates Risk Priority Number (RPN) and maps corrective actions."""
        rpn = severity * occurrence * detection
        action_required = rpn >= self.config["dfmea_critical_rpn_threshold"]
        
        entry = {
            "component": self.config["component_name"],
            "mechanism": mechanism,
            "rpn": rpn,
            "action_required": action_required,
            "status": "OPEN" if action_required else "MONITOR"
        }
        self.failure_log.append(entry)
        return entry

    def export_to_dvp(self, output_path: str):
        """Exports logs to a DVP&R tracking dataframe."""
        df = pd.DataFrame(self.failure_log)
        df.to_csv(output_path, index=False)
      
