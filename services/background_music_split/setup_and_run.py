import subprocess
import os
import sys

def check_conda_installed():
    """Check if conda is installed"""
    try:
        subprocess.run(["conda", "--version"], check=True, stdout=subprocess.PIPE)
        print("Conda is installed.")
    except subprocess.CalledProcessError:
        print("Conda is not installed. Please install Miniconda or Anaconda.")
        sys.exit(1)

def create_conda_environment(env_name, python_version="3.9"):
    """Create a new conda environment if it doesn't exist"""
    try:
        subprocess.run(["conda", "create", "--name", env_name, f"python={python_version}", "-y"], check=True)
        print(f"Created conda environment '{env_name}' with Python {python_version}.")
    except subprocess.CalledProcessError:
        print(f"Failed to create conda environment '{env_name}'.")
        sys.exit(1)

def install_required_packages(env_name):
    """Install required packages in the conda environment"""
    try:
        subprocess.run(["conda", "activate", env_name, "&&", "conda", "install", "spleeter", "numpy", "-y"], shell=True, check=True)
        print("Packages installed successfully in the conda environment.")
    except subprocess.CalledProcessError:
        print("Failed to install required packages.")
        sys.exit(1)

def run_audio_split_script():
    """Run the audio_split.py script"""
    try:
        subprocess.run(["python", "/Users/danm/youtube_dubbing_project/services/background_music_split/audio_split.py"], check=True)
        print("Audio split script executed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to execute the audio split script.")
        sys.exit(1)

if __name__ == "__main__":
    check_conda_installed()
    environment_name = "video-dubbing"

    # Check if the environment exists, create it if not
    try:
        subprocess.run(["conda", "info", "--envs"], check=True, stdout=subprocess.PIPE)
        print(f"Checking if environment {environment_name} exists.")
        if environment_name not in str(subprocess.check_output(["conda", "info", "--envs"])):
            print(f"Environment '{environment_name}' not found. Creating it now.")
            create_conda_environment(environment_name)
        else:
            print(f"Environment '{environment_name}' already exists.")
    except subprocess.CalledProcessError:
        print("Error while checking conda environments. Exiting.")
        sys.exit(1)

    # Install packages and run the script
    install_required_packages(environment_name)
    run_audio_split_script()
