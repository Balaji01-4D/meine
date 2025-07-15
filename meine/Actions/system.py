import asyncio
import datetime as dt
import os
import platform
import subprocess
from time import ctime

import psutil
from rich.console import Group
from rich.panel import Panel
from rich.progress import BarColumn, Progress
from rich.table import Table

from ..exceptions import InfoNotify
from .other import SizeHelper
from .app_theme import get_theme_colors


class System:

    os_type = platform.system()

    def safe_style(self, style_name):
        """Safely get a style from theme, with fallback to default colors if there's an error"""
        if not hasattr(self, "_theme_colors"):
            self._theme_colors = get_theme_colors()

        return self._theme_colors.get(style_name, "white")

    def ShutDown(self):

        if self.os_type == "Windows":
            os.system(r"shutdown \s \t 60")
            raise InfoNotify("shutting down in 1 Minute")
        elif self.os_type == "Linux" or self.os_type == "Darwin":
            os.system("shutdown -h +1")
            raise InfoNotify("shutting down in 1 Minute")
        else:
            raise InfoNotify("Unsupported OS")

    def Reboot(self):

        if self.os_type == "Windows":
            os.system(r"shutdown \r \t 60")
            raise InfoNotify("restarting in 1 Minute")
        elif self.os_type == "Linux" or self.os_type == "Darwin":
            os.system("shutdown -r +1")
            raise InfoNotify("restarting in 1 Minute")
        else:
            raise InfoNotify("Unsupported OS")

    async def Time(self) -> Panel:
        date = dt.datetime.now().date()
        time = dt.datetime.now().time()
        try:
            if not hasattr(self, "_theme_colors"):
                self._theme_colors = get_theme_colors()
            return f"""[{self._theme_colors['accent']}]DATE : {date}\nTIME : {time}"""
        except Exception:
            return f"DATE : {date}\nTIME : {time}"

    async def IP(self) -> Table:
        import socket

        try:
            if not hasattr(self, "_theme_colors"):
                self._theme_colors = get_theme_colors()
            primary = self._theme_colors["primary"]
            accent = self._theme_colors["accent"]
            foreground = self._theme_colors["foreground"]

            hostname = socket.gethostname()
            net_if_addrs = psutil.net_if_addrs()
            fqdn = await asyncio.to_thread(socket.getfqdn)

            ip_address_task = asyncio.to_thread(socket.gethostbyname, hostname)
            ip_address = await ip_address_task

            net_info = Table(
                show_header=False,
                show_lines=True,
                title=f"[{accent}]Network Information",
                border_style=primary,
            )

            net_info.add_row("Hostname", hostname, style=foreground)
            net_info.add_row("FQDN", fqdn, style=foreground)
            net_info.add_row("Primary IP", ip_address, style=foreground)

            try:

                active_interfaces = []
                for interface, addrs in net_if_addrs.items():
                    for addr in addrs:
                        if (
                            addr.family == socket.AF_INET
                            and not addr.address.startswith("127.")
                        ):
                            active_interfaces.append((interface, addr.address))
                            break

                if active_interfaces:
                    net_info.add_row("", "", style=foreground)
                    net_info.add_row(
                        f"[{accent}]Active Interfaces", "", style=foreground
                    )
                    for interface, addr in active_interfaces:
                        net_info.add_row(f"  {interface}", addr, style=foreground)
            except Exception:
                pass

            if_types = {
                socket.AF_INET: "IPv4",
                socket.AF_INET6: "IPv6",
                getattr(socket, "AF_PACKET", None): "Hardware",
                getattr(socket, "AF_LINK", None): "Hardware",
            }

            ipv4_count = 0
            ipv6_count = 0
            hw_count = 0

            for interface, addrs in net_if_addrs.items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        ipv4_count += 1
                    elif addr.family == socket.AF_INET6:
                        ipv6_count += 1
                    elif addr.family in [
                        getattr(socket, "AF_PACKET", None),
                        getattr(socket, "AF_LINK", None),
                    ]:
                        hw_count += 1

            net_info.add_row("", "", style=foreground)
            net_info.add_row(f"[{accent}]Interface Summary", "", style=foreground)
            net_info.add_row("  IPv4 Addresses", str(ipv4_count), style=foreground)
            net_info.add_row("  IPv6 Addresses", str(ipv6_count), style=foreground)
            net_info.add_row("  Hardware Addresses", str(hw_count), style=foreground)

            localhost_info = socket.gethostbyname_ex("localhost")
            
            if localhost_info and len(localhost_info) > 2:
                net_info.add_row("", "", style=foreground)
                net_info.add_row(
                    f"[{accent}]Localhost",
                    ", ".join(localhost_info[2]),
                    style=foreground,
                )

            return net_info

        except Exception as e:
            raise InfoNotify(f"Error in Fetching IP: {e}")

    async def ram_info(self) -> Panel:
        try:
            primary = self.safe_style("primary")
            accent = self.safe_style("accent")
            foreground = self.safe_style("foreground")

            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()

            total = memory.total
            available = memory.available
            used = memory.used
            free = memory.free
            active = getattr(memory, "active", 0)
            inactive = getattr(memory, "inactive", 0)
            buffers = getattr(memory, "buffers", 0)
            cached = getattr(memory, "cached", 0)
            shared = getattr(memory, "shared", 0)

            data = {
                "AVAILABLE": available / total * 100,
                "USED": used / total * 100,
                "CACHED": cached / total * 100 if cached else 0,
                "BUFFER": buffers / total * 100 if buffers else 0,
            }

            rampanel = Progress(
                "[progress.description]{task.description}",
                BarColumn(bar_width=30, complete_style=accent),
                "{task.percentage:>3.0f}%",
            )

            rampanel.add_task(
                f"[{foreground}]AVAILABLE % ", total=100, completed=data["AVAILABLE"]
            )
            rampanel.add_task(
                f"[{foreground}]USED      % ", total=100, completed=data["USED"]
            )

            if cached:
                rampanel.add_task(
                    f"[{foreground}]CACHED    % ", total=100, completed=data["CACHED"]
                )
            if buffers:
                rampanel.add_task(
                    f"[{foreground}]BUFFER    % ", total=100, completed=data["BUFFER"]
                )

            ram_table = Table(show_lines=True, border_style=primary)
            ram_table.add_column("Memory Type", style=foreground, header_style=accent)
            ram_table.add_column("Size", style=foreground, header_style=accent)
            ram_table.add_column("Percentage", style=foreground, header_style=accent)

            ram_table.add_row("Total", SizeHelper(total), "100%")
            ram_table.add_row("Used", SizeHelper(used), f"{used/total*100:.1f}%")
            ram_table.add_row(
                "Available", SizeHelper(available), f"{available/total*100:.1f}%"
            )
            ram_table.add_row("Free", SizeHelper(free), f"{free/total*100:.1f}%")

            if active:
                ram_table.add_row(
                    "Active", SizeHelper(active), f"{active/total*100:.1f}%"
                )
            if inactive:
                ram_table.add_row(
                    "Inactive", SizeHelper(inactive), f"{inactive/total*100:.1f}%"
                )
            if cached:
                ram_table.add_row(
                    "Cached", SizeHelper(cached), f"{cached/total*100:.1f}%"
                )

            ram_table.add_row("Swap Total", SizeHelper(swap.total), "")
            ram_table.add_row(
                "Swap Used", SizeHelper(swap.used), f"{swap.percent:.1f}%"
            )
            ram_table.add_row(
                "Swap Free", SizeHelper(swap.free), f"{100-swap.percent:.1f}%"
            )

            ram_info_text = (
                f"[{foreground}]Total Memory      : [{accent}]{SizeHelper(total)}\n"
                f"[{foreground}]Memory Available  : [{accent}]{SizeHelper(available)}\n"
                f"[{foreground}]Memory Used       : [{accent}]{SizeHelper(used)}\n"
                f"[{foreground}]Memory Free       : [{accent}]{SizeHelper(free)}\n"
                f"[{foreground}]Swap Used         : [{accent}]{SizeHelper(swap.used)} of {SizeHelper(swap.total)}"
            )

            panel_group = Group(
                Panel(f"[{accent}]RAM INFORMATION", width=20, border_style=primary),
                Panel(rampanel, width=70, border_style=primary),
                Panel(ram_info_text, width=70, border_style=primary),
                Panel(
                    ram_table,
                    width=70,
                    border_style=primary,
                    title=f"[{accent}]Detailed Memory Statistics",
                ),
            )

            return panel_group
        except Exception as e:
            return Panel(f"Error getting RAM information: {e}", border_style=primary)

    async def SYSTEM(self) -> Panel:
        try:
            primary = self.safe_style("primary")
            accent = self.safe_style("accent")
            foreground = self.safe_style("foreground")
            error = self.safe_style("error")

            cpu_percent = asyncio.to_thread(psutil.cpu_percent, 1)
            memory = psutil.virtual_memory()
            boot_time = psutil.boot_time()
            disk_usage = psutil.disk_usage("/")
            users = await asyncio.to_thread(psutil.users)
            cpu_freq = psutil.cpu_freq()

            os_art = ""
            os_name = platform.system()

            if os_name == "Linux":
                os_art = rf"""[{accent}]
         _nnnn_
        dGGGGMMb
       @p~qp~~qMb
       M|@||@) M|
       @,----.JM|
      JS^\\_/  qKL
     dZP        qKRb
    dZP          qKKb
   fZP            SMMb
   HZM            MMMM
   FqM            MMMM
 __| ".        |\dS"qML
 |    `.       | `' \Zq
_)      \.___.,|     .'
\____   )MMMMMP|   .'
     `-'       `--'
                """
            elif os_name == "Windows":
                os_art = rf"""[{accent}]
        ,.=:^^!t3Z3z.,
       :tt:::tt333EE3
       Et:::ztt33EEE  @Ee.,
      ;tt:::tt333EE7 ;EEEEEEttttt33#
     :Et:::zt333EEQ. $EEEEEttttt33QL
     it::::tt333EEF @EEEEEEttttt33F
    ;3=*^```"*4EEV :EEEEEEttttt33@.
    ,.=::::it=.,   @EEEEEEtttz33QF
   ;::::::::zt33)   "4EEEtttji3P*
  :t::::::::tt33.Z3z..  `` ,..g.
  i::::::::zt33F AEEEtttt::::ztF
 ;:::::::::t33V ;EEEttttt::::t3
 E::::::::zt33L @EEEtttt::::z3F
*3=*^```"*4E3) ;EEEtttt:::::tZ`
             `` :EEEEtttt::::z7
                 "VEzjt:;;z>*`
                """
            elif os_name == "Darwin":
                os_art = rf"""[{accent}]
                .:'
              __ :'__
           .'`__`-'__``.
          :__________.-'
          :_________:
           :_________`-;
            `._.-._.'
                """
            else:
                os_art = f"""[{accent}]
         _nnnn_
        dGGGGMMb
       @p~qp~~qMb
       M|@||@) M|
       @,----.JM|
      JS^\\_/  qKL
     dZP        qKRb
    dZP          qKKb
   fZP            SMMb
   HZM            MMMM
   FqM            MMMM
 __| ".        |\\dS"qML
 |    `.       | `' \\Zq
_)      \\.___.,|     .'
\\____   )MMMMMP|   .'
     `-'       `--'
                """

            uptime_seconds = int(dt.datetime.now().timestamp() - boot_time)
            uptime_days = uptime_seconds // 86400
            uptime_hours = (uptime_seconds % 86400) // 3600
            uptime_minutes = (uptime_seconds % 3600) // 60
            uptime_str = f"{uptime_days}d {uptime_hours}h {uptime_minutes}m"

            hostname = platform.node()
            username = os.environ.get("USER", os.environ.get("USERNAME", "user"))

            user_host = f"[{accent}]{username}[{foreground}]@[{accent}]{hostname}"

            separator = f"[{accent}]" + "-" * (len(username) + len(hostname) + 1)

            sys_info = []
            sys_info.append(
                f"[{accent}]         OS:[{foreground}] {platform.system()} {platform.release()}"
            )
            sys_info.append(f"[{accent}]Kernel:[{foreground}] {platform.version()}")
            sys_info.append(f"[{accent}]Uptime:[{foreground}] {uptime_str}")

            cpu_model = ""
            if self.os_type == "Linux":
                try:
                    with open("/proc/cpuinfo", "r") as f:
                        for line in f:
                            if line.startswith("model name"):
                                cpu_model = line.split(":", 1)[1].strip()
                                break
                except:
                    cpu_model = platform.processor()
            else:
                cpu_model = platform.processor()

            cpu_freq_str = ""
            if cpu_freq and hasattr(cpu_freq, "current") and cpu_freq.current:
                if cpu_freq.current > 1000:
                    cpu_freq_str = f" @ {cpu_freq.current/1000:.2f} GHz"
                else:
                    cpu_freq_str = f" @ {cpu_freq.current:.0f} MHz"

            sys_info.append(f"[{accent}]CPU:[{foreground}] {cpu_model}{cpu_freq_str}")
            sys_info.append(f"[{accent}]CPU Usage:[{foreground}] {cpu_percent}%")

            total_mem_gb = memory.total / (1024**3)
            used_mem_gb = memory.used / (1024**3)
            sys_info.append(
                f"[{accent}]Memory:[{foreground}] {used_mem_gb:.1f}GB / {total_mem_gb:.1f}GB ({memory.percent}%)"
            )

            total_disk_gb = disk_usage.total / (1024**3)
            used_disk_gb = disk_usage.used / (1024**3)
            sys_info.append(
                f"[{accent}]Disk (/):[{foreground}] {used_disk_gb:.1f}GB / {total_disk_gb:.1f}GB ({disk_usage.percent}%)"
            )

            try:
                if self.os_type == "Linux":
                    res_output = subprocess.check_output(
                        "xrandr | grep '\\*'", shell=True
                    ).decode()
                    resolution = res_output.split()[0]
                    sys_info.append(f"[{accent}]Resolution:[{foreground}] {resolution}")
            except:
                pass

            shell = os.environ.get("SHELL", "")
            if shell:
                shell_name = os.path.basename(shell)
                sys_info.append(f"[{accent}]Shell:[{foreground}] {shell_name}")

            terminal = os.environ.get("TERM", "")
            if terminal:
                sys_info.append(f"[{accent}]Terminal:[{foreground}] {terminal}")

            os_art_lines = os_art.strip().split("\n")
            art_width = max(len(line) for line in os_art_lines)

            padded_art_lines = []
            for line in os_art_lines:

                padded_art_lines.append(f"{line:<{art_width}}")

            lines = []

            max_lines = max(len(padded_art_lines), len(sys_info))
            for i in range(max_lines):
                art_line = (
                    padded_art_lines[i]
                    if i < len(padded_art_lines)
                    else " " * art_width
                )
                info_line = sys_info[i] if i < len(sys_info) else ""

                lines.append(f"{art_line}    {info_line}")

            lines.insert(0, user_host)
            lines.insert(1, separator)
            lines.insert(2, "")

            neofetch_panel = Panel(
                "\n".join(lines),
                title=f"[{accent}]System Information",
                border_style=primary,
                padding=(1, 2),
            )

            progress = Progress(
                "{task.description}",
                BarColumn(bar_width=40, complete_style=accent),
                "{task.percentage:>3.0f}%",
                expand=True,
            )

            cpu_task = progress.add_task(
                f"[{foreground}]CPU Usage", total=100, completed=cpu_percent
            )
            mem_task = progress.add_task(
                f"[{foreground}]Memory Usage", total=100, completed=memory.percent
            )
            disk_task = progress.add_task(
                f"[{foreground}]Disk Usage", total=100, completed=disk_usage.percent
            )

            progress_panel = Panel(
                progress, title=f"[{accent}]System Resources", border_style=primary
            )

            system_group = Group(neofetch_panel, progress_panel)

            return system_group
        except Exception as e:
            return Panel(f"Error getting system information: {e}", border_style="red")

    async def Battery(self) -> Panel:
        try:
            primary = self.safe_style("primary")
            accent = self.safe_style("accent")
            foreground = self.safe_style("foreground")
            error = self.safe_style("error")

            battery = await asyncio.to_thread(psutil.sensors_battery)

            if battery:

                percent = round(battery.percent)
                is_charging = battery.power_plugged
                status = "Charging" if is_charging else "Discharging"

                time_left_str = "Unknown"
                if battery.secsleft > 0 and not is_charging:
                    hours, remainder = divmod(battery.secsleft, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    time_left_str = f"{int(hours)}h {int(minutes)}m"
                elif is_charging:
                    time_left_str = "Charging"
                elif battery.secsleft == -1:
                    time_left_str = "Calculating..."

                battery_art = self._get_battery_ascii(percent, is_charging)

                battery_info = []

                status_icon = "⚡ " if is_charging else ""
                battery_info.append(
                    f"[{accent}]Status:[{foreground}] {status_icon}{status}"
                )
                battery_info.append(f"[{accent}]Percentage:[{foreground}] {percent}%")
                battery_info.append(
                    f"[{accent}]Time left:[{foreground}] {time_left_str}"
                )

                if self.os_type == "Linux":
                    try:

                        if os.path.exists("/sys/class/power_supply/BAT0/"):
                            bat_path = "/sys/class/power_supply/BAT0/"

                            try:
                                with open(f"{bat_path}manufacturer", "r") as f:
                                    manufacturer = f.read().strip()
                                    if manufacturer:
                                        battery_info.append(
                                            f"[{accent}]Manufacturer:[{foreground}] {manufacturer}"
                                        )
                            except:
                                pass

                            try:
                                with open(f"{bat_path}model_name", "r") as f:
                                    model = f.read().strip()
                                    if model:
                                        battery_info.append(
                                            f"[{accent}]Model:[{foreground}] {model}"
                                        )
                            except:
                                pass

                            try:
                                with open(f"{bat_path}technology", "r") as f:
                                    technology = f.read().strip()
                                    if technology:
                                        battery_info.append(
                                            f"[{accent}]Technology:[{foreground}] {technology}"
                                        )
                            except:
                                pass

                            try:
                                with open(f"{bat_path}energy_full_design", "r") as f:
                                    design_capacity = int(f.read().strip()) / 1000000
                                    battery_info.append(
                                        f"[{accent}]Design capacity:[{foreground}] {design_capacity:.2f} Wh"
                                    )
                            except:
                                pass

                            try:
                                with open(f"{bat_path}energy_full", "r") as f:
                                    full_capacity = int(f.read().strip()) / 1000000
                                    with open(f"{bat_path}energy_now", "r") as f2:
                                        current_energy = (
                                            int(f2.read().strip()) / 1000000
                                        )
                                        battery_info.append(
                                            f"[{accent}]Current capacity:[{foreground}] {current_energy:.2f}/{full_capacity:.2f} Wh"
                                        )

                                        if "Design capacity" in "\n".join(battery_info):
                                            health = (
                                                full_capacity / design_capacity
                                            ) * 100
                                            battery_info.append(
                                                f"[{accent}]Health:[{foreground}] {health:.1f}%"
                                            )
                            except:
                                pass

                            try:
                                with open(f"{bat_path}cycle_count", "r") as f:
                                    cycles = f.read().strip()
                                    battery_info.append(
                                        f"[{accent}]Charge cycles:[{foreground}] {cycles}"
                                    )
                            except:
                                pass
                    except:
                        pass

                lines = []

                status_text = f"[{accent}]              Status: [{foreground}]{status}"

                if is_charging:
                    percent_text = f"[{accent}]⚡ Percentage: [{foreground}]{percent}%"
                else:
                    percent_text = f"[{accent}]Percentage: [{foreground}]{percent}%"

                time_text = f"[{accent}]Time left: [{foreground}]{time_left_str}"

                lines.append(status_text)
                lines.append(percent_text)
                lines.append(time_text)

                separator_line = "─" * 10
                lines.append(f"[{accent}]{separator_line}")

                battery_art_lines = battery_art.strip().split("\n")

                if self.os_type == "Linux":

                    try:
                        with open(
                            "/sys/class/power_supply/BAT0/manufacturer", "r"
                        ) as f:
                            manufacturer = f.read().strip()
                            if manufacturer:
                                lines.append(
                                    f"[{accent}]Manufacturer: [{foreground}]{manufacturer}"
                                )
                    except:
                        pass

                    try:
                        with open("/sys/class/power_supply/BAT0/model_name", "r") as f:
                            model = f.read().strip()
                            if model:
                                lines.append(f"[{accent}]Model: [{foreground}]{model}")
                    except:
                        pass

                    try:
                        with open("/sys/class/power_supply/BAT0/technology", "r") as f:
                            technology = f.read().strip()
                            if technology:
                                lines.append(
                                    f"[{accent}]Technology: [{foreground}]{technology}"
                                )
                    except:
                        pass

                    try:
                        with open(
                            "/sys/class/power_supply/BAT0/energy_full_design", "r"
                        ) as f:
                            design_capacity = int(f.read().strip()) / 1000000
                            lines.append(
                                f"[{accent}]Design capacity: [{foreground}]{design_capacity:.2f} Wh"
                            )
                    except:
                        pass

                    try:
                        with open("/sys/class/power_supply/BAT0/energy_full", "r") as f:
                            full_capacity = int(f.read().strip()) / 1000000
                            with open(
                                "/sys/class/power_supply/BAT0/energy_now", "r"
                            ) as f2:
                                current_energy = int(f2.read().strip()) / 1000000
                                lines.append(
                                    f"[{accent}]Current capacity: [{foreground}]{current_energy:.2f}/{full_capacity:.2f} Wh"
                                )

                                try:
                                    with open(
                                        "/sys/class/power_supply/BAT0/energy_full_design",
                                        "r",
                                    ) as f3:
                                        design_capacity = (
                                            int(f3.read().strip()) / 1000000
                                        )
                                        health = (full_capacity / design_capacity) * 100
                                        lines.append(
                                            f"[{accent}]Health: [{foreground}]{health:.1f}%"
                                        )
                                except:
                                    pass
                    except:
                        pass

                    try:
                        with open("/sys/class/power_supply/BAT0/cycle_count", "r") as f:
                            cycles = f.read().strip()
                            lines.append(
                                f"[{accent}]Charge cycles: [{foreground}]{cycles}"
                            )
                    except:
                        pass

                art_and_info = []
                for i, art_line in enumerate(battery_art_lines):
                    if i < len(lines):
                        art_and_info.append(f"{art_line}  {lines[i]}")
                    else:
                        art_and_info.append(art_line)

                battery_panel = Panel(
                    "\n".join(art_and_info),
                    title=f"[{accent}]Battery Information",
                    border_style=primary,
                    padding=(1, 2),
                )

                progress = Progress(
                    "{task.description}",
                    BarColumn(
                        bar_width=40, complete_style=self._get_battery_color(percent)
                    ),
                    "{task.percentage:>3.0f}%",
                    expand=True,
                )

                battery_task = progress.add_task(
                    f"[{foreground}]Battery Level", total=100, completed=percent
                )

                progress_panel = Panel(
                    progress, title=f"[{accent}]Power Status", border_style=primary
                )

                battery_group = Group(battery_panel, progress_panel)

                return battery_group

            return Panel(
                f"[{error}]No battery information available.", border_style=primary
            )
        except Exception as e:
            return Panel(f"Error getting battery information: {e}", border_style="red")

    def _get_battery_ascii(self, percent, is_charging):
        """Generate ASCII art for battery based on charge level and charging status"""
        accent = self.safe_style("accent")

        if percent >= 90:
            return f"""[{accent}]
 ___________ 
|           |
|           |
|███████████|
|███████████|
|███████████|
|___________|"""
        elif percent >= 75:
            return f"""[{accent}]
 ___________ 
|           |
|           |
|█████████  |
|█████████  |
|█████████  |
|___________|"""
        elif percent >= 50:
            return f"""[{accent}]
 ___________ 
|           |
|           |
|██████     |
|██████     |
|██████     |
|___________|"""
        elif percent >= 25:
            return f"""[{accent}]
 ___________ 
|           |
|           |
|████       |
|████       |
|████       |
|___________|"""
        else:
            return f"""[{accent}]
 ___________ 
|           |
|           |
|█          |
|█          |
|█          |
|___________|"""

    def _get_battery_color(self, percent):
        """Return an appropriate color based on battery percentage"""
        if percent <= 10:
            return "red"
        elif percent <= 25:
            return "yellow"
        else:
            return self.safe_style("accent")

    async def ENV(self) -> Table:
        try:
            primary = self.safe_style("primary")
            accent = self.safe_style("accent")
            foreground = self.safe_style("foreground")

            env_vars = await asyncio.to_thread(os.environ.items)

            env = Table(show_lines=True, title=f"[{accent}]ENV", border_style=primary)
            env.add_column("key", no_wrap=True, header_style=accent)
            env.add_column("value", no_wrap=True, header_style=accent)

            for key, value in env_vars:
                env.add_row(key, value, style=foreground)

            return env
        except Exception as e:
            return Table(
                title=f"Error getting environment variables: {e}", border_style="red"
            )

    async def CPU(self) -> Panel:
        try:
            primary = self.safe_style("primary")
            accent = self.safe_style("accent")
            foreground = self.safe_style("foreground")

            cpu_tasks = [
                asyncio.to_thread(psutil.cpu_percent, interval=0.5),
                asyncio.to_thread(psutil.cpu_percent, interval=0.5, percpu=True),
            ]

            if platform.system() != "Windows":
                cpu_tasks.append(asyncio.to_thread(psutil.cpu_stats))
                cpu_tasks.append(asyncio.to_thread(psutil.cpu_times_percent))

            results = await asyncio.gather(*cpu_tasks)

            overall_usage = results[0]
            per_cpu = results[1]
            cpu_count_physical = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count(logical=True)

            cpu_freq = psutil.cpu_freq()

            components = []

            overall_progress = Progress(
                "[progress.description]{task.description}",
                BarColumn(bar_width=30, complete_style=accent),
                "{task.percentage:>3.0f}%",
            )
            overall_progress.add_task(
                f"[{foreground}]CPU OVERALL % ", total=100, completed=overall_usage
            )
            components.append(
                Panel(
                    overall_progress,
                    border_style=primary,
                    title=f"[{accent}]Overall CPU Usage",
                )
            )

            per_core_progress = Progress(
                "[progress.description]{task.description}",
                BarColumn(bar_width=20, complete_style=accent),
                "{task.percentage:>3.0f}%",
            )

            cores_to_display = min(len(per_cpu), 8)
            for i in range(cores_to_display):
                per_core_progress.add_task(
                    f"[{foreground}]Core {i} ", total=100, completed=per_cpu[i]
                )

            if len(per_cpu) > cores_to_display:
                components.append(
                    Panel(
                        per_core_progress,
                        border_style=primary,
                        title=f"[{accent}]Per-Core Usage (showing {cores_to_display} of {len(per_cpu)} cores)",
                    )
                )
            else:
                components.append(
                    Panel(
                        per_core_progress,
                        border_style=primary,
                        title=f"[{accent}]Per-Core Usage",
                    )
                )

            cpu_info_table = Table(show_lines=True, border_style=primary)
            cpu_info_table.add_column(
                "CPU Property", style=foreground, header_style=accent
            )
            cpu_info_table.add_column("Value", style=foreground, header_style=accent)

            cpu_info_table.add_row(
                "Physical Cores",
                str(cpu_count_physical) if cpu_count_physical else "N/A",
            )
            cpu_info_table.add_row(
                "Logical Cores", str(cpu_count_logical) if cpu_count_logical else "N/A"
            )

            if cpu_freq:
                if hasattr(cpu_freq, "current") and cpu_freq.current:
                    cpu_info_table.add_row(
                        "Current Frequency", f"{cpu_freq.current:.2f} MHz"
                    )
                if hasattr(cpu_freq, "min") and cpu_freq.min:
                    cpu_info_table.add_row("Min Frequency", f"{cpu_freq.min:.2f} MHz")
                if hasattr(cpu_freq, "max") and cpu_freq.max:
                    cpu_info_table.add_row("Max Frequency", f"{cpu_freq.max:.2f} MHz")

            if len(results) > 4 and results[4]:
                cpu_stats = results[4]
                if hasattr(cpu_stats, "ctx_switches"):
                    cpu_info_table.add_row(
                        "Context Switches", f"{cpu_stats.ctx_switches:,}"
                    )
                if hasattr(cpu_stats, "interrupts"):
                    cpu_info_table.add_row("Interrupts", f"{cpu_stats.interrupts:,}")

            components.append(
                Panel(
                    cpu_info_table,
                    border_style=primary,
                    title=f"[{accent}]CPU Specifications",
                )
            )

            if len(results) > 5 and results[5]:
                cpu_times = results[5]
                cpu_time_table = Table(show_lines=True, border_style=primary)
                cpu_time_table.add_column(
                    "CPU Time", style=foreground, header_style=accent
                )
                cpu_time_table.add_column(
                    "Percentage", style=foreground, header_style=accent
                )

                important_times = ["user", "system", "idle"]
                for time_type in important_times:
                    if hasattr(cpu_times, time_type):
                        value = getattr(cpu_times, time_type)
                        cpu_time_table.add_row(time_type.capitalize(), f"{value:.1f}%")

                components.append(
                    Panel(
                        cpu_time_table,
                        border_style=primary,
                        title=f"[{accent}]CPU Time Distribution",
                    )
                )

            arch_info = Panel(
                f"[{foreground}]Architecture: [{accent}]{platform.machine()}\n"
                f"[{foreground}]Processor: [{accent}]{platform.processor()}",
                border_style=primary,
            )
            components.append(arch_info)

            if self.os_type == "Linux":
                try:
                    with open("/proc/cpuinfo", "r") as f:
                        for line in f:
                            if line.startswith("model name"):
                                model = line.split(":", 1)[1].strip()
                                components.append(
                                    Panel(
                                        f"[{foreground}]CPU Model: [{accent}]{model}",
                                        border_style=primary,
                                    )
                                )
                                break
                except:
                    pass

            components.insert(0, f"[{accent}]CPU INFORMATION")

            return Group(*components)
        except Exception as e:
            return Panel(f"Error getting CPU information: {e}", border_style="red")

    async def USER(self) -> Panel:
        try:
            if self.os_type in ["Linux", "Darwin"]:
                return await self._get_user_info_unix()
            else:
                return await self._get_user_info_windows()
        except Exception as e:
            return Panel(
                f"Error getting user information: {e}",
                border_style=self.safe_style("error"),
            )
    
    async def _get_user_info_unix(self) -> Panel:
        import getpass, os, pwd, grp, psutil
        from time import ctime

        primary = self.safe_style("primary")
        accent = self.safe_style("accent")
        foreground = self.safe_style("foreground")

        username = getpass.getuser()
        user_info = pwd.getpwnam(username)

        user_table = Table(show_header=False, show_lines=True, border_style=primary)
        user_table.add_column("Property", style=primary)
        user_table.add_column("Value", style=foreground)

        user_table.add_row("Username", username)
        user_table.add_row("User ID", str(user_info.pw_uid))
        user_table.add_row("Group ID", str(user_info.pw_gid))
        user_table.add_row("Home Directory", user_info.pw_dir)
        user_table.add_row("Shell", user_info.pw_shell)
        user_table.add_row("Full Name", user_info.pw_gecos.split(",")[0])

        try:
            groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
            main_group = grp.getgrgid(user_info.pw_gid).gr_name
            if main_group not in groups:
                groups.append(main_group)
            user_table.add_row("Groups", ", ".join(groups))
        except:
            pass

        try:
            users = await asyncio.to_thread(psutil.users)
            for user in users:
                if user.name == username:
                    user_table.add_row("Terminal", getattr(user, "terminal", "N/A"))
                    user_table.add_row("Host", getattr(user, "host", "localhost"))
                    if hasattr(user, "started"):
                        user_table.add_row("Login Time", ctime(user.started))
                    break
        except:
            pass

        env_keys = ["USER", "USERNAME", "HOME", "LOGNAME", "PATH"]
        for key in env_keys:
            val = os.environ.get(key)
            if val:
                user_table.add_row(f"Env: {key}", val)

        return Panel(user_table, title=f"[{accent}]User Information", border_style=primary)


    async def DiskInfo(self):
        try:
            primary = self.safe_style("primary")
            accent = self.safe_style("accent")
            foreground = self.safe_style("foreground")
            secondary = self.safe_style("secondary")
            error = self.safe_style("error")

            partition_table = Table(
                show_lines=True,
                border_style=primary,
                title=f"[{accent}]Disk Partitions",
            )

            headers = ["Device", "Mount Point", "Total Size", "Used", "Free", "Usage"]
            for header in headers:
                partition_table.add_column(
                    header, style=foreground, header_style=accent
                )

            io_table = Table(
                show_lines=True,
                border_style=primary,
                title=f"[{accent}]Disk I/O Statistics",
            )

            io_headers = [
                "Device",
                "Read Count",
                "Write Count",
                "Read Bytes",
                "Write Bytes",
                "Read Time",
                "Write Time",
            ]
            for header in io_headers:
                io_table.add_column(header, style=foreground, header_style=accent)

            partitions = await asyncio.to_thread(psutil.disk_partitions, all=True)

            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    partition_table.add_row(
                        partition.device,
                        partition.mountpoint,
                        f"{usage.total / (1024 ** 3):.2f} GB",
                        f"{usage.used / (1024 ** 3):.2f} GB",
                        f"{usage.free / (1024 ** 3):.2f} GB",
                        f"{usage.percent}%",
                    )
                except (PermissionError, OSError):

                    partition_table.add_row(
                        partition.device,
                        partition.mountpoint,
                        "N/A",
                        "N/A",
                        "N/A",
                        f"[{error}]No access",
                    )
                    continue

            disk_io = await asyncio.to_thread(psutil.disk_io_counters, perdisk=True)

            if disk_io:
                for disk_name, stats in disk_io.items():
                    io_table.add_row(
                        disk_name,
                        f"{stats.read_count:,}",
                        f"{stats.write_count:,}",
                        f"{stats.read_bytes / (1024 ** 2):.2f} MB",
                        f"{stats.write_bytes / (1024 ** 2):.2f} MB",
                        (
                            f"{stats.read_time} ms"
                            if hasattr(stats, "read_time")
                            else "N/A"
                        ),
                        (
                            f"{stats.write_time} ms"
                            if hasattr(stats, "write_time")
                            else "N/A"
                        ),
                    )

            tables = []
            tables.append(partition_table)
            tables.append(io_table)

            try:
                space_progress = Progress(
                    "{task.description}",
                    BarColumn(bar_width=None),
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    "[{task.completed:.2f} GB of {task.total:.2f} GB]",
                    expand=True,
                )

                for partition in partitions:
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        total_gb = usage.total / (1024**3)
                        used_gb = usage.used / (1024**3)

                        if total_gb > 1:
                            task_id = space_progress.add_task(
                                f"[{accent}]{partition.device} ({partition.mountpoint})",
                                total=total_gb,
                                completed=used_gb,
                            )
                    except (PermissionError, OSError):
                        continue

                progress_panel = Panel(
                    space_progress,
                    title=f"[{accent}]Disk Usage",
                    border_style=primary,
                    padding=(1, 2),
                )
                tables.insert(0, progress_panel)
            except Exception:

                pass

            return Group(*tables)
        except Exception as e:
            return Panel(
                f"Error getting disk information: {e}",
                title="Disk Info Error",
                border_style=self.safe_style("error"),
            )
        
    async def _get_user_info_windows(self) -> Panel:
        import getpass, os, psutil
        from time import ctime

        primary = self.safe_style("primary")
        accent = self.safe_style("accent")
        foreground = self.safe_style("foreground")

        username = getpass.getuser()

        user_table = Table(show_header=False, show_lines=True, border_style=primary)
        user_table.add_column("Property", style=primary)
        user_table.add_column("Value", style=foreground)

        user_table.add_row("Username", username)

        env_keys = ["USER", "USERNAME", "USERPROFILE", "HOME", "LOGNAME", "PATH"]
        for key in env_keys:
            val = os.environ.get(key)
            if val:
                user_table.add_row(f"Env: {key}", val)

        home_dir = os.path.expanduser("~")
        if home_dir:
            user_table.add_row("Home Directory", home_dir)

        try:
            users = await asyncio.to_thread(psutil.users)
            for user in users:
                if user.name == username:
                    user_table.add_row("Terminal", getattr(user, "terminal", "N/A"))
                    user_table.add_row("Host", getattr(user, "host", "localhost"))
                    if hasattr(user, "started"):
                        user_table.add_row("Login Time", ctime(user.started))
                    break
        except:
            pass

        return Panel(user_table, title=f"[{accent}]User Information", border_style=primary)


    async def Processes(self):
        try:
            primary = self.safe_style("primary")
            accent = self.safe_style("accent")
            foreground = self.safe_style("foreground")

            tableofproccess = Table(show_lines=True, border_style=primary)
            headers = ["PID", "Name", "Status", "Memory (RAM)", "CPU Usage (%)"]

            for header in headers:
                tableofproccess.add_column(
                    header, style=foreground, header_style=accent
                )

            for proc in psutil.process_iter(
                attrs=["pid", "name", "status", "memory_info"]
            ):
                try:
                    pid = proc.info["pid"]
                    name = proc.info["name"]
                    status = proc.info["status"]
                    memory = proc.info["memory_info"].rss / (1024 * 1024)
                    cpu_usage = proc.cpu_percent(interval=0.1)
                    tableofproccess.add_row(
                        str(pid),
                        name,
                        str(status),
                        f"{memory:.2f} MB",
                        f"{cpu_usage:.2f}%",
                    )

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    pass

            return tableofproccess
        except Exception as e:
            return Table(
                title=f"Error getting process information: {e}", border_style="red"
            )

    async def ProcessKill(self, pid):
        try:
            process = psutil.Process(pid)
            await asyncio.to_thread(process.kill)
            return f"Process with PID {pid} has been terminated."
        except psutil.NoSuchProcess:
            return f"No process with PID {pid} exists."
        except psutil.AccessDenied:
            return f"Permission denied to terminate the process {pid}."
        except Exception as e:
            return f"Error terminating process {pid}: {e}"

    def refresh_theme(self):
        """Refresh the cached theme colors"""
        self._theme_colors = get_theme_colors()
        return self._theme_colors
