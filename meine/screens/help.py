from pathlib import Path

from textual.screen import ModalScreen
from textual.widgets import MarkdownViewer


HELP_MANUAL = """\

# Directory Tree

## Key Bindings


- **Ctrl + D**: Toggle the directory tree.
- **Mouse Click**: Move to the currently focused directory.
- **Home Key**: Move directly to the home directory.
- **Ctrl + Click**: Copy the name of the directory or file to the input console.
- **Ctrl + r**: Refresh the directory tree.
- **Ctrl + M**: open the system utils screen.
## Note

- Changing the directory in the directory tree will also update the **current working directory**.
  - **Example**: Using the directory tree to change a directory is equivalent to executing the `cd` command in the terminal.

---

# Input Console Help

## Command Reference

### **Delete Command**

| Action     | Command                                       |
|-------------|-----------------------------------------------|
| Single     | `d`, `rm`, `r`, `del <file/folder name>`      |
| Multiple   | `d`, `rm`, `r`, `del <file1>, <file2>, ...`   |

### **Create Command**

| Action     | Command                                       |
|-------------|-----------------------------------------------|
| Single     | `mk (or) create <filename>`, `mkdir|mkd <foldername>`|
| Multiple   | `mk (or) create <filename1>, <filename2>, ...`, `mkdir|mkd <foldername1>, <foldername2>, ...` |

### **Rename Command**

| Action     | Command                                        |
|-------------|-----------------------------------------------|
| Single     | `rn (or) rename <oldname> as <newname>`             |
| Multiple   | `rn (or) rename <oldname1>, <oldname2>, ... as <newname1>, <newname2>, ...` |

### **Copy Command**

| Action     | Command                                       |
|-------------|-----------------------------------------------|
| Single     | `cp (or) c (or) copy <source> to <destination>`         |
| Multiple   | `cp (or) c (or) copy <source1>, <source2>, ... to <destination>` |

### **Move Command**

| Action     | Command                                       |
|-------------|-----------------------------------------------|
| Single     | `mv (or) m (or) move <source> to <destination>`         |
| Multiple   | `mv (or) m (or) move <source1>, <source2>, ... to <destination>` |

### **Search Text Command**

| Action     | Command                                       |
|-------------|-----------------------------------------------|
| Folder     | `search (or) find (or) where "text" <folder path>`      |
| File       | `search (or) find (or) where "text" <file path>`        |

 """


class HelpScreen(ModalScreen[None]):

    CSS_PATH = Path(__file__).parent.parent / "tcss/help.tcss"

    def compose(self):
        yield MarkdownViewer(HELP_MANUAL)
