# 🔍 Peekr

**Peekr** is a lightweight command-line utility for searching files or directories based on name patterns, last accessed time, type, and max traversal depth.

---

## Features

-  Search for files or directories by name pattern
-  Filter by last accessed time (in days)
-  Limit search depth
-  Choose between file or directory matches

---

##  Usage

```bash
python peekr.py [options] [search_directory]
```

If search_directory is not provided, it defaults to the current directory (.).

---

## ️ Options

|Option | Description |
|---|---|
|-n, -name | (Required) Pattern to match filenames (e.g. *.txt)|
|-atime <days> | Only show files accessed within the last <days> days|
|-t, -type| `<f(default) | d>`|
|-m, --max-depth | Maximum depth of directory traversal (default is 1)|

---

##  Examples
- Find all .py files in the current directory:
    ```bash
    python peekr.py -n "*.py"
    ```

- Search inside /home/user/projects for directories accessed in the last 5 days:
    ```bash
    python peekr.py -n "*" -t d -atime 5 /home/user/projects
    ```
---

## 👨‍💻 Author
Developed by [epicboi-deepubhai](https://github.com/epicboi-deepubhai)
