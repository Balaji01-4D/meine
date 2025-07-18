# System Commands

Meine provides a comprehensive set of system commands to monitor and manage your system resources. This guide covers all available system commands and their usage.

::: info
**New in v2.0.0:** 
- System utility widgets now support live reload
- Press `Ctrl + M` to access the system utility screen
- Select widgets from an elegant dropdown menu
- Command-line access to system utilities has been removed

For complete details about v2.0.0 changes, visit: [v2.0.0 Release Notes](https://github.com/Balaji01-4D/meine/releases/tag/v2.0.0)
:::

## System Information

### CPU Information

```bash
# Show CPU usage and stats
cpu
```

::: warning
**Removed in v2.0.0:**
Command-line access to this utility has been completely removed. Please use the system utility screen (`Ctrl + M`) and select "CPU" from the dropdown.
:::

Output includes:
- CPU usage percentage (overall and per-core)
- Physical and logical CPU count
- CPU frequency range
- CPU model information
- CPU architecture
- CPU time distribution (user, system, idle)

### Memory Information

```bash
# Show memory usage
ram
```

::: warning
**Removed in v2.0.0:**
Command-line access to this utility has been completely removed. Please use the system utility screen (`Ctrl + M`) and select "RAM" from the dropdown.
:::

Output includes:
- Total memory capacity
- Used memory with percentage
- Available memory with percentage
- Free memory with percentage
- Swap usage statistics
- Memory visualization with progress bars
- Cached and buffer memory (on supported systems)
- Active and inactive memory details
- Detailed memory statistics table
- Memory usage trends


### Battery Status

```bash
# Show battery information
battery
```

::: warning
**Removed in v2.0.0:**
Command-line access to this utility has been completely removed. Please use the system utility screen (`Ctrl + M`) and select "Battery" from the dropdown.
:::

Output includes:
- Battery percentage with color-coded status
- Charging status (charging/discharging)
- Remaining time estimate
- Battery health percentage (on supported systems)
- Battery manufacturer and model (on Linux)
- ASCII art representation of battery level
- Charge cycles information
- Battery capacity details (design vs. current)

### Network Information

```bash
# Show network information
ip
```

::: warning
**Removed in v2.0.0:**
Command-line access to this utility has been completely removed. Please use the system utility screen (`Ctrl + M`) and select "Network" from the dropdown.
:::

Output includes:
- Hostname and FQDN
- Primary IP address
- Active network interfaces
- IPv4 and IPv6 addresses
- Hardware addresses
- Interface summary statistics
- Localhost information

<!-- ### GPU Information

```bash
# Show GPU information
gpu

# Available options:
gpu --detailed    # Show detailed GPU information
gpu --processes   # Show GPU usage by process
gpu --memory      # Show GPU memory usage
```

Output includes:
- GPU model
- Driver version
- Temperature
- Memory usage
- Active processes -->

::: info
**Coming Soon:**
GPU monitoring features will be available in a future release. All system widgets are now accessed through the system utility screen (`Ctrl + M`), providing a more interactive experience with a dropdown widget selector.
:::


### System Overview

```bash
# Show complete system information (similar to neofetch)
system
```

::: warning
**Removed in v2.0.0:**
Command-line access to this utility has been completely removed. Please use the system utility screen (`Ctrl + M`) and select "System Overview" from the dropdown. It is inspired by Neofetch.
:::


Output includes:
- OS type and version with ASCII art logo
- Kernel information
- System uptime
- CPU model and usage
- Memory statistics
- Disk usage
- Network information
- Current user
- Visual progress bars for system resources


### Environment Variables

```bash
# Show environment variables
env
```

::: warning
**Removed in v2.0.0:**
Command-line access to this utility has been completely removed. Please use the system utility screen (`Ctrl + M`) and select "Environment Variables" from the dropdown.
:::


Output includes:
- Complete list of environment variables
- Key-value pairs in tabular format
- Organized display with syntax highlighting


### User Information

```bash
# Show user information
user
```

::: warning
**Removed in v2.0.0:**
Command-line access to this utility has been completely removed. Please use the system utility screen (`Ctrl + M`) and select "User Details" from the dropdown.
:::


Output includes:
- Username and user ID
- Group memberships
- Home directory location
- Shell information
- Login time and terminal
- Environment variables related to user
- Full name and account details

The user command is cross-platform compatible, displaying relevant information on both Windows and Unix-like systems (Linux/macOS).

### List Processes

```bash
# Show running processes
process
```

::: warning
**Removed in v2.0.0:**
this utility is completely removed, will be added in the future release.
:::


Output includes:
- Process ID (PID)
- Process name
- Current status
- Memory usage (RAM)
- CPU usage percentage
- Organized in a sortable table



### Disk Usage

```bash
# Show disk usage
disk
```

::: warning
**Removed in v2.0.0:**
Command-line access to this utility has been completely removed. Please use the system utility screen (`Ctrl + M`) and select "Disk Storage" from the dropdown.
:::


Output includes:
- Mounted partitions with paths
- Total, used, and free space for each disk
- Usage percentage with visual indicators
- Disk I/O statistics (read/write)
- Disk throughput information
- Progress bars for visual representation
- Detailed information about disk types

## New System Utility Screen (v2.0.0+)

The new system utility screen provides a centralized interface for accessing all system widgets with a live reload feature.

### Accessing the System Utility Screen

Press `Ctrl + M` from anywhere in Meine to open the system utility screen.

### Widget Selection Dropdown

The system utility screen features an elegant dropdown menu as shown below:


The dropdown menu includes the following options:

- **Select** - Default dropdown state
- **System Overview** - Comprehensive system information (similar to Neofetch)
- **CPU Information** - Detailed CPU usage and specifications
- **RAM Usage** - Memory statistics and visualizations
- **Disk Storage** - Storage utilization and I/O statistics
- **Network Configuration** - Network interfaces and connection data
- **Battery Status** - Battery health and power information
- **User Details** - Current user account information
- **Environment Variables** - System environment variables list

::: tip
**Quick Widget Access:**
Simply click on the dropdown and select the desired widget. Each widget will automatically load with real-time data.
:::

### Live Reload Feature

::: tip
**Real-Time Updates:**
All widgets in the system utility screen automatically refresh with real-time data. The refresh interval can be adjusted in the settings panel.
:::

### Keyboard Navigation

Navigate between widgets using these keyboard shortcuts:

- `Tab` / `Shift+Tab` - Move between interface elements
- `Up`/`Down` Arrow keys - Navigate dropdown options
- `Enter` - Select the highlighted widget
- `Esc` - Close the dropdown menu
- `Ctrl+M` - Toggle system utility screen
