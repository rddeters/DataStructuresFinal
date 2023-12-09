class InsuranceInformation:
    def __init__(self, primary_name, provider_name, policy_number, vision_coverage, medical_coverage, copay=None):
        self.primary_name = primary_name  # Initialize the primary name associated with the insurance
        self.provider_name = self.validate_optional_string(provider_name, "Provider Name")  # Validate/store ins name
        self.policy_number = self.validate_optional_string(policy_number, "Policy Number")  # Validate/store policy num
        self.vision_coverage = vision_coverage  # Store vision coverage information
        self.medical_coverage = medical_coverage  # Store medical coverage information
        self.copay = self.validate_optional_int(copay)  # Validate and store copay (optional)

    @staticmethod
    def validate_optional_string(value, field_name):
        # Static method to validate and clean an optional string field
        if value == "N/A":
            return None  # If "N/A" is provided, treat it as None
        if not value.strip():  # Check for an empty string
            raise ValueError(f"{field_name} must be entered or 'N/A'.")
        if not all(char.isalnum() or char in " '-" for char in value):
            raise ValueError(f"{field_name} contains invalid characters.")
        return value

    @staticmethod
    def validate_optional_int(value):
        # Static method to validate and clean an optional integer field
        if value == "N/A":
            return None  # If "N/A" is provided, treat it as None
        if not value.strip():  # Check for an empty string
            raise ValueError("Copay must be entered or 'N/A'.")
        try:
            return int(value)  # Convert the value to an integer
        except ValueError:
            raise ValueError("Copay must be an integer or 'N/A'.")
