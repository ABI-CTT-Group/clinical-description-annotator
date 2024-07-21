def is_observation_type(variable):
    if isinstance(variable, dict):
        required_keys = {"value_system", "value", "code", "units_system", "units"}

        if required_keys.issubset(variable.keys()):
            if isinstance(variable["value"], (int, float, str)) and \
                    isinstance(variable["value_system"], str) and \
                    isinstance(variable["code"], str) and \
                    isinstance(variable["units_system"], str) and \
                    isinstance(variable["units"], str):
                return True
    return False
