"""
Pulsar Trophy Editor Trophy Monarch
sponsored by ChatGPT o4-mini-high
Pulsar Intel sponsored by Github Copilot
"""
import os
import re
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox

class SaveEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trophy Monarch by Gab")

        # Data structures
        self.rows = []  # each: {'id', 'path', 'vars', 'lbl_name', 'orig_flags'}
        self.translations = {}  # ID (uppercase) -> "Name (ID)"

        # --- Menu ---
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Folder...", command=self.open_folder)
        file_menu.add_command(label="Load Translation File...", command=self.load_translation)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.tools_menu = tk.Menu(menubar, tearoff=0)
        # Keep track of menu item indices
        self.tools_menu.add_command(label="Update Settings File...", command=self.update_settings_file)
        self.tools_menu.add_separator()
        self.tools_menu.add_command(label="Show Current Trophy Count...", command=self.show_trophy_count)
        self.tools_menu.add_separator()
        self.tools_menu.add_command(label="Show Unrecognized Tracks...", command=self.show_unrecognized_count)
        self.tools_menu.add_command(label="Uncheck Unrecognized Tracks...", command=self.uncheck_unrecognized)
        # Initially disable Update Settings (index 0)
        self.tools_menu.entryconfig(0, state='disabled')
        self.tools_menu.entryconfig(4, state='disabled')  # Show Unrecognized Tracks
        self.tools_menu.entryconfig(5, state='disabled')  # Uncheck Unrecognized Tracks
        menubar.add_cascade(label="Tools", menu=self.tools_menu)
        root.config(menu=menubar)

        # --- Controls Frame ---
        ctrl_frame = tk.Frame(root)
        ctrl_frame.pack(fill=tk.X, padx=5, pady=5)

        # Set-all buttons for each trophy column
        for i in range(4):
            btn = tk.Button(ctrl_frame, text=f"Set All Trophy {i+1}",
                            command=lambda idx=i: self.set_all(idx))
            btn.pack(side=tk.LEFT, padx=2)

        # Save button
        self.save_btn = tk.Button(ctrl_frame, text="Save Changes", command=self.confirm_save)
        self.save_btn.pack(side=tk.RIGHT, padx=2)

        # --- Scrollable List ---
        container = tk.Frame(root)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.list_frame = tk.Frame(canvas)

        self.list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Column headers
        hdrs = ["Track ID", "Track Name"] + [f"Trophy {i+1}" for i in range(4)]
        for col, text in enumerate(hdrs):
            tk.Label(self.list_frame, text=text, font=('Arial', 10, 'bold')).grid(
                row=0, column=col, padx=5, pady=2
            )

    def open_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        self.base_folder = folder
        self.clear_rows()
        for sub in os.listdir(folder):
            subpath = os.path.join(folder, sub)
            if os.path.isdir(subpath):
                fpath = os.path.join(subpath, 'ldb.pul')
                if os.path.isfile(fpath):
                    flags = self.read_flags(fpath)
                    self.add_row(sub, fpath, flags)
        state = 'normal' if self.rows else 'disabled'
        self.tools_menu.entryconfig(0, state=state)
        self.adjust_window_width()

    def read_flags(self, filepath):
        with open(filepath, 'rb') as f:
            f.seek(0x3C)
            data = f.read(4)
        return [b != 0 for b in data]

    def add_row(self, track_id, path, flags):
        # track_id kept as-is for display, but uppercase for lookup
        row = {
            'id': track_id,
            'path': path,
            'orig_flags': flags,
            'vars': [tk.BooleanVar(value=val) for val in flags]
        }
        r = len(self.rows) + 1
        tk.Label(self.list_frame, text=track_id).grid(row=r, column=0, padx=5, pady=2)
        # Lookup translation by uppercase ID
        name = self.translations.get(track_id.upper(), track_id)
        lbl_name = tk.Label(self.list_frame, text=name)
        lbl_name.grid(row=r, column=1, padx=5, pady=2)
        row['lbl_name'] = lbl_name

        for i in range(4):
            tk.Checkbutton(
                self.list_frame,
                variable=row['vars'][i]
            ).grid(row=r, column=2+i, padx=5)

        self.rows.append(row)

    def clear_rows(self):
        for child in self.list_frame.winfo_children():
            child.destroy()
        self.rows.clear()
        hdrs = ["Track ID", "Track Name"] + [f"Trophy {i+1}" for i in range(4)]
        for col, text in enumerate(hdrs):
            tk.Label(self.list_frame, text=text, font=('Arial', 10, 'bold')).grid(
                row=0, column=col, padx=5, pady=2
            )

    def set_all(self, col_idx):
        for row in self.rows:
            row['vars'][col_idx].set(True)

    def load_translation(self):
        path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        if not path:
            return
        self.translations.clear()
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '=' not in line:
                    continue
                name_part, id_part = line.split('=', 1)
                tid = id_part.strip().upper()
                name = re.sub(r'\\c\{.*?\}', '', name_part).strip()
                self.translations[tid] = f"{name} ({tid})"
        # Update UI and count unrecognized
        unrecognized = 0
        for row in self.rows:
            up_id = row['id'].upper()
            if up_id in self.translations:
                row['lbl_name'].config(text=self.translations[up_id])
            else:
                unrecognized += 1
                row['lbl_name'].config(text=row['id'])
        if unrecognized:
            messagebox.showinfo(
                "Translation Load",
                f"Translation loaded. {unrecognized} tracks could not be matched."  
            )
        # Enable unrecognized actions
        self.tools_menu.entryconfig(4, state='normal')
        self.tools_menu.entryconfig(5, state='normal')
        self.adjust_window_width()

    def uncheck_unrecognized(self):
        # Uncheck all trophy boxes for rows without a translation
        count = 0
        for row in self.rows:
            if row['id'].upper() not in self.translations:
                for var in row['vars']:
                    if var.get():
                        var.set(False)
                        count += 1
        messagebox.showinfo(
            "Uncheck Unrecognized",
            f"Unchecked {count} trophy flags across unrecognized tracks."
        )

    def adjust_window_width(self):
        # Resize window based on widest column
        self.root.update_idletasks()
        col_count = 6  # Track ID, Track Name, 4 trophies
        max_widths = [0] * col_count
        for widget in self.list_frame.winfo_children():
            info = widget.grid_info()
            col = int(info.get('column', 0))
            if isinstance(widget, tk.Label):
                font = tkfont.Font(font=widget.cget('font'))
                text = widget.cget('text')
                w = font.measure(text)
                if w > max_widths[col]:
                    max_widths[col] = w
        # Sum column widths + padding
        total = sum(max_widths)
        pad = col_count * 20 + 20  # ~5px padding each side per column
        scrollbar_width = 20
        new_width = total + pad + scrollbar_width
        height = self.root.winfo_height()
        self.root.geometry(f"{new_width}x{height}")

    def show_unrecognized_count(self):
        # Count rows without a translation match
        unrecognized = sum(1 for row in self.rows if row['id'].upper() not in self.translations)
        messagebox.showinfo("Unrecognized Tracks", f"{unrecognized} tracks have no translation.")

    def confirm_save(self):
        if not self.rows:
            messagebox.showwarning("No files", "No ldb.pul files loaded to save.")
            return
        paths = [row['path'] for row in self.rows]
        total = len(paths)
        # Show only first 5 paths, then indicate how many more
        display_list = paths if total <= 5 else paths[:5] + [f"and {total - 5} more files."]
        msg = "The following paths will be modified:\n" + "\n".join(display_list)
        if not messagebox.askokcancel("Save Confirmation", msg):
            return
        self.perform_save()

    def perform_save(self):
        for row in self.rows:
            data = bytes(1 if var.get() else 0 for var in row['vars'])
            with open(row['path'], 'r+b') as f:
                f.seek(0x3C)
                f.write(data)
        messagebox.showinfo("Done", "All files updated successfully.")

    def show_trophy_count(self):
        # Calculate current counts for each trophy column
        counts = [sum(1 for row in self.rows if row['vars'][i].get()) for i in range(4)]
        msg = (
            f"Current Trophy Counts:\n"
            f"Trophy 1: {counts[0]}\n"
            f"Trophy 2: {counts[1]}\n"
            f"Trophy 3: {counts[2]}\n"
            f"Trophy 4: {counts[3]}"
        )
        messagebox.showinfo("Current Trophy Count", msg)

    def update_settings_file(self):
        path = filedialog.askopenfilename(filetypes=[('PUL Files', '*.pul'), ('All Files', '*.*')])
        if not path:
            return
        # Load entire file into mutable bytearray
        with open(path, 'rb') as f:
            data = bytearray(f.read())
        header = b"TROP"
        idx = data.find(header)
        if idx == -1:
            messagebox.showerror("Error", '"TROP" header not found in file.')
            return
        # Update trophy counts (2 bytes each, big-endian) at corrected offsets
        counts = [sum(1 for row in self.rows if row['vars'][i].get()) for i in range(4)]
        # New offsets based on XX location for low byte of Trophy1
        offsets = [0x0C, 0x0E, 0x10, 0x12]
        for i, cnt in enumerate(counts):
            off = idx + offsets[i]
            data[off:off+2] = cnt.to_bytes(2, 'big')
        # Build map of track ID bytes to BooleanVar lists
        id_map = {}
        for row in self.rows:
            try:
                tid_bytes = bytes.fromhex(row['id'])
                if len(tid_bytes) == 4:
                    id_map[tid_bytes] = row['vars']
            except ValueError:
                continue
        # Scan 8-byte blocks after offset idx+0x20 until footer
        footer = b"\x47\x50\x00\x00\x00\x00\x00\x01"
        pos = idx + 0x14
        while pos + 8 <= len(data):
            block = bytes(data[pos:pos+8])
            if block == footer:
                break
            # Original layout: first 4 bytes = track ID, next 4 bytes = status
            id_block = block[:4]
            vars_list = id_map.get(id_block)
            if vars_list:
                status_bytes = bytes(1 if v.get() else 0 for v in vars_list)
                data[pos+4:pos+8] = status_bytes
            pos += 8
        # Write back without changing file length
        with open(path, 'r+b') as f:
            f.seek(0)
            f.write(data)
            f.truncate()
        messagebox.showinfo("Done", "Settings file updated successfully.")

if __name__ == '__main__':
    root = tk.Tk()
    app = SaveEditorApp(root)
    root.mainloop()
