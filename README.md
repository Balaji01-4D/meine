<h1 align="center">MEINE 🌒</h1>

<p align="center">
  <strong>A modern, regex-powered file manager and system utility for the terminal.</strong><br>
  Combining intuitive command parsing with a rich TUI to make terminal operations fast and beautiful.
</p>

<div align="center">
<a href="https://github.com/Balaji01-4D/meine/stargazers">
  <img src="https://img.shields.io/github/stars/Balaji01-4D/meine" alt="Stars Badge"/>
</a>
<a href="https://github.com/Balaji01-4D/meine/issues">
  <img src="https://img.shields.io/github/issues/Balaji01-4D/meine" alt="Issues Badge"/>
</a>
<a href="https://github.com/Balaji01-4D/meine/graphs/contributors">
  <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/Balaji01-4D/meine?color=2b9348"/>
</a>
<a href="https://github.com/Balaji01-4D/meine/blob/master/LICENSE">
  <img src="https://img.shields.io/github/license/Balaji01-4D/meine?color=2b9348" alt="License Badge"/>
</a>
<img src="https://static.pepy.tech/badge/meine?color=2b9348" alt="Downloads Badge"/>

<p>
  <img alt="Meine Demo" src="img/intro.gif" width="80%" />
  <br><em>Intuitive Terminal Interface</em>
</p>

<p>
  <img alt="Widgets Demo" src="img/widgets.gif" width="80%" />
  <br><em>Rich System Widgets</em>
</p>

<p>
  <img alt="Windows Utilities Demo" src="img/window_utils_live.gif" width="80%" />
  <br><em>Cross-Platform Compatibility</em>
</p>

<p><i>Loved the project? Please consider <a href="https://ko-fi.com/balaji01">donating</a> to help it improve!</i></p>

</div>


## Features

- **Regex-Based Command Parsing**  
  Use intuitive commands to delete, copy, move, rename, search, and create files or folders.

- **TUI Directory Navigator**  
  Browse your filesystem in a reactive terminal UI—keyboard and mouse supported.

- **Live Command Console**  
  A built-in shell for interpreting commands and reflecting state changes in real time.

- **Asynchronous & Modular**  
  Built with `asyncio`, `aiofiles`, `py7zr`, and modular architecture for responsive performance.

- **Theming & Config**  
  CSS-powered themes, JSON-based user preferences, and dynamic runtime settings.

- **System Dashboard**  
  Real-time system insights via one-liner commands:
  `cpu`, `ram`, `battery`, `ip`, `user`, `env`, and more.

- **Plugin Ready**  
  Drop in your own Python modules to extend functionality without altering core logic.

---
## Screenshots

<details open>
<summary><b>Main Interface</b></summary>
<p align="center">
  <img src="https://github.com/Balaji01-4D/meine/blob/main/img/new1.png" alt="Input shell" width="45%" hspace="10">
  <img src="https://github.com/Balaji01-4D/meine/blob/main/img/widgets/settinng_screen.png" alt="Settings screen" width="45%" hspace="10">
</p>

<p align="center">
  <b>Input Shell</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Settings screen</b>
</p>
</details>

<details open>
<summary><b>System Utilities</b></summary>
<p align="center">
  <img src="https://github.com/Balaji01-4D/meine/blob/main/img/widgets/system_info.png" alt="System widget" width="80%">
</p>

<p align="center"><b>System widget (inspired by Neofetch)</b></p>

<p align="center">
  <img src="https://github.com/Balaji01-4D/meine/blob/main/img/new2.png" alt="Dynamic Suggestions" width="80%">
</p>

<p align="center"><b>Dynamic Suggestions</b></p>
</details>

<details>
<summary><b>Hardware Monitoring</b></summary>
<p align="center">
  <img src="https://github.com/Balaji01-4D/meine/blob/main/img/widgets/battery_updated.png" alt="Battery widget" width="80%">
</p>

<p align="center"><b>Battery widget</b></p>

<p align="center">
  <img src="https://github.com/Balaji01-4D/meine/blob/main/img/widgets/ram.png" alt="RAM widget" width="80%">
</p>

<p align="center"><b>RAM widget</b></p>

<p align="center">
  <img src="https://github.com/Balaji01-4D/meine/blob/main/img/widgets/cpu.png" alt="CPU widget" width="80%">
</p>

<p align="center"><b>CPU widget</b></p>
</details>

---

## Installation

<details open>
<summary><b>Quick Install</b></summary>

**Install via pip**
> Requires Python 3.10+

```bash
pip install meine
```
</details>

<details>
<summary><b>From Source</b></summary>

```bash
git clone https://github.com/Balaji01-4D/meine
cd meine
pip install .
```
</details>

---

## Regex-Based Commands

<table>
<thead>
  <tr>
    <th>Action</th>
    <th>Syntax Examples</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><b>Delete</b></td>
    <td><code>del file.txt</code> &nbsp;·&nbsp; <code>rm file1.txt,file2.txt</code></td>
  </tr>
  <tr>
    <td><b>Copy</b></td>
    <td><code>copy a.txt to b.txt</code> &nbsp;·&nbsp; <code>cp a1.txt,a2.txt to d/</code></td>
  </tr>
  <tr>
    <td><b>Move</b></td>
    <td><code>move a.txt to d/</code> &nbsp;·&nbsp; <code>mv f1.txt,f2.txt to ../</code></td>
  </tr>
  <tr>
    <td><b>Rename</b></td>
    <td><code>rename old.txt as new.txt</code></td>
  </tr>
  <tr>
    <td><b>Create</b></td>
    <td><code>mk file.txt</code> &nbsp;·&nbsp; <code>mkdir folder1,folder2</code></td>
  </tr>
  <tr>
    <td><b>Search</b></td>
    <td><code>search "text" folder/</code> &nbsp;·&nbsp; <code>find "term" notes.md</code></td>
  </tr>
</tbody>
</table>

---

<p align="center">
  <sub>© 2025 MEINE | Made with 🌒  by Balaji J | <a href="https://github.com/Balaji01-4D/meine/blob/master/LICENSE">MIT License</a></sub>
</p>