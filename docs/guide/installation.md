# Installation

## Requirements

- Python 3.10 or higher
- pip (Python package installer)
- Git (optional, for development)

## Installation Methods

### 1. Using pip (Recommended)

The easiest way to install **Meine** is via pip:

```bash
pip install meine
````

### 2. From Source

To install the latest development version or contribute to the project:

```bash
# Clone the repository
git clone https://github.com/Balaji01-4D/meine
cd meine

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Verifying Installation

To confirm Meine is installed correctly:

```bash
meine --version
```

You should see the version number displayed in the output.

::: tip
If the command isn't found, try:
1. Restarting your terminal
2. Checking if Python's bin directory is in your PATH
3. Using the full path: `python -m meine --version`
:::

## Platform-Specific Notes

::: info
Python 3.10+ is required for all platforms.
:::

### Linux

* May require additional packages like `psutil` for system monitoring
* Install build essentials for compiling native extensions:
  ```bash
  sudo apt-get install build-essential python3-dev  # For Debian/Ubuntu
  sudo dnf install gcc python3-devel                # For Fedora/RHEL
  ```

### macOS

* Requires the Xcode command-line tools for native extensions:
  ```bash
  xcode-select --install
  ```
* Some system utilities require admin privileges

### Windows

* Use Windows Terminal or PowerShell for the best experience
* Install Visual C++ Build Tools for native extensions:
  ```
  pip install --upgrade setuptools
  ```
* System monitoring features have limited support compared to Unix-like systems

## Troubleshooting

::: warning
Always check for error messages in the terminal output for specific issues.
:::

If you run into problems during installation:

1. **Check Python version**

   ```bash
   python --version  # Should show 3.10 or higher
   ```
   
   If the command isn't found or shows an older version, you may need to use `python3` instead:
   
   ```bash
   python3 --version
   ```

2. **Update pip**

   ```bash
   python -m pip install --upgrade pip
   ```

3. **Fix permission errors**

   ```bash
   pip install --user meine
   ```
   
   On Linux/macOS, you might need sudo (not recommended for Python packages):
   ```bash
   sudo pip install meine  # Use only if necessary
   ```

4. **Virtual environment issues**

   ```bash
   python -m pip install virtualenv
   python -m virtualenv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install meine
   ```

5. **Missing dependencies**

   If you see errors about missing dependencies:
   
   ```bash
   pip install --upgrade setuptools wheel
   ```
   
   For native extension errors:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-dev

   # Fedora/RHEL
   sudo dnf install python3-devel
   
   # Windows
   # Install Visual Studio Build Tools with C++ workload
   ```

6. **Path issues**

   If the `meine` command isn't found after installation, add the Python scripts directory to your PATH.
   

