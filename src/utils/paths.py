"""
Utility function to get project root directory for consistent paths
"""
import os

def get_project_root():
    """
    Get the project root directory (TradingAiCode folder)
    Works from any subdirectory in the project
    """
    current_file = os.path.abspath(__file__)
    
    # Go up directories until we find the project root
    # (directory containing README.md and main scripts)
    current_dir = os.path.dirname(current_file)
    
    while current_dir != os.path.dirname(current_dir):  # Not at filesystem root
        if os.path.exists(os.path.join(current_dir, 'README.md')) and \
           os.path.exists(os.path.join(current_dir, 'CollectStocksData.py')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    
    # Fallback: assume we're in project root
    return os.getcwd()

def get_data_dir(data_type="raw"):
    """
    Get data directory path within project
    
    Args:
        data_type: "raw", "features", "enhanced"
    
    Returns:
        Absolute path to data directory
    """
    project_root = get_project_root()
    
    if data_type == "raw":
        return os.path.join(project_root, "MarketData")
    elif data_type == "features":
        return os.path.join(project_root, "MarketData_Features")
    elif data_type == "enhanced":
        return os.path.join(project_root, "MarketData_Features_Enhanced")
    else:
        return os.path.join(project_root, "data", data_type)

def get_models_dir():
    """Get models directory path within project"""
    return os.path.join(get_project_root(), "models")

def get_outputs_dir():
    """Get outputs directory path within project"""
    return os.path.join(get_project_root(), "outputs")

if __name__ == "__main__":
    print(f"Project root: {get_project_root()}")
    print(f"Raw data: {get_data_dir('raw')}")
    print(f"Features: {get_data_dir('features')}")
    print(f"Models: {get_models_dir()}")
    print(f"Outputs: {get_outputs_dir()}")
