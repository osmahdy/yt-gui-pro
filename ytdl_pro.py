import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import threading
import json
import re

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DocumentationWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Developer Documentation & Guide")
        self.geometry("750x620")
        self.resizable(True, True)

        self.title_label = ctk.CTkLabel(self, text="YouTube Downloader Pro - Docs", font=("Helvetica", 22, "bold"))
        self.title_label.pack(pady=15)

        self.textbox = ctk.CTkTextbox(self, width=700, height=500, font=("Arial", 16))
        self.textbox.pack(padx=20, pady=10, fill="both", expand=True)
        
        docs_content = """=== 1. Overview ===
This program is a GUI built with Python (CustomTkinter) acting as a wrapper for 'yt-dlp' and FFmpeg.
Supports automatic URL detection for single videos or full Playlists with a large font interface.

=== 2. Code Structure & Modification Guide ===
- Automatic Playlist Detection: Checks if 'playlist' or 'list=' exists in the pasted URL.
- Safe JSON Parsing: Prevents 'NoneType' errors when fetching playlist entries.
- fetch_qualities: Dynamically handles both formats and playlist items.
- run_download: Manages single and batch playlist downloading with exclusion filters.
"""
        self.textbox.insert("0.0", docs_content)
        self.textbox.configure(state="disabled")

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader Pro")
        self.geometry("780x800")
        self.resizable(True, True)

        self.current_font_size = 18
        self.title_font_size = 26

        self.url_var = ctk.StringVar()
        self.folder_var = ctk.StringVar()
        self.qualities_dict = {}
        self.playlist_entries = []
        self.video_checkboxes = []

        self.favorite_paths = [
            "/home/black/Downloads",
            "/home/black/Storage/UNIVERSITY",
            "/home/black/Desktop"
        ]
        
        # Top Bar
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=30, pady=(15, 0))
        
        self.title_label = ctk.CTkLabel(self.top_frame, text="YouTube Downloader Pro", font=("Helvetica", self.title_font_size, "bold"))
        self.title_label.pack(side="left")
        
        self.top_right_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        self.top_right_frame.pack(side="right")

        self.font_label = ctk.CTkLabel(self.top_right_frame, text="Font:", font=("Arial", 14, "bold"))
        self.font_label.pack(side="left", padx=(0, 5))

        self.font_menu = ctk.CTkComboBox(self.top_right_frame, values=["Base (18)", "Large (20)", "X-Large (22)"], command=self.change_font_size, width=140, height=38, font=("Arial", 14))
        self.font_menu.pack(side="left", padx=(0, 10))
        self.font_menu.set("Base (18)")

        self.docs_btn = ctk.CTkButton(self.top_right_frame, text="DOCS 📖", command=self.open_docs, width=90, height=38, font=("Arial", 14, "bold"), fg_color="#4158D0", hover_color="#3043C8")
        self.docs_btn.pack(side="left")

        # URL Input Section
        self.url_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.url_frame.pack(fill="x", padx=30, pady=12)
        
        self.url_entry = ctk.CTkEntry(self.url_frame, textvariable=self.url_var, width=540, height=50, font=("Arial", self.current_font_size))
        self.url_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        self.setup_placeholder(self.url_entry, "Paste YouTube video or playlist link here...")
        
        self.fetch_btn = ctk.CTkButton(self.url_frame, text="Fetch Data", command=self.fetch_qualities, width=160, height=50, font=("Arial", self.current_font_size, "bold"))
        self.fetch_btn.pack(side="left")

        # Save Folder Section
        self.folder_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.folder_frame.pack(fill="x", padx=30, pady=12)
        
        self.folder_entry = ctk.CTkEntry(self.folder_frame, textvariable=self.folder_var, width=400, height=50, font=("Arial", self.current_font_size))
        self.folder_entry.pack(side="left", padx=(0, 10), fill="x", expand=True)
        self.setup_placeholder(self.folder_entry, "Select save folder...")
        
        self.path_menu = ctk.CTkComboBox(self.folder_frame, values=["Quick Paths ▼"] + self.favorite_paths, command=self.on_path_selected, width=150, height=50, font=("Arial", 14))
        self.path_menu.pack(side="left", padx=(0, 5))

        # Quality Selection Section
        self.quality_label = ctk.CTkLabel(self, text="Select Video Quality:", font=("Arial", 16, "bold"))
        self.quality_label.pack(anchor="w", padx=35, pady=(15, 5))
        
        self.quality_menu = ctk.CTkComboBox(self, values=["Fetch data first..."], width=720, height=50, font=("Arial", self.current_font_size), state="disabled")
        self.quality_menu.pack(padx=30, pady=5, fill="x")

        # Playlist Collapsible Frame (تظهر تلقائياً إذا كان الرابط بلايليست)
        self.playlist_preview_frame = ctk.CTkFrame(self, fg_color=("gray85", "gray20"))
        self.preview_header_btn = ctk.CTkButton(self, text="▶ Playlist Videos List (Click to Expand)", command=self.toggle_playlist_preview, fg_color="transparent", text_color=("black", "white"), anchor="w", font=("Arial", 15, "bold"))
        
        self.playlist_scroll_frame = ctk.CTkScrollableFrame(self.playlist_preview_frame, width=700, height=150)
        self.playlist_scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.is_preview_open = False

        # Progress Bar & Status
        self.progress_bar = ctk.CTkProgressBar(self, width=720, height=18)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=30, pady=(20, 10), fill="x")

        self.status_label = ctk.CTkLabel(self, text="Ready to download", font=("Arial", 15), text_color="gray")
        self.status_label.pack(padx=30, pady=2)

        # Download Button
        self.download_btn = ctk.CTkButton(self, text="Start Download", command=self.start_download_thread, width=300, height=58, font=("Arial", 18, "bold"), fg_color="#2fa572", hover_color="#248259")
        self.download_btn.pack(pady=15)

    def is_playlist_url(self, url):
        """التحقق التلقائي مما إذا كان الرابط يحتوي على بلايليست"""
        return "playlist" in url.lower() or "list=" in url.lower()

    def toggle_playlist_preview(self):
        if not self.is_preview_open:
            self.playlist_preview_frame.pack(padx=30, pady=8, fill="x")
            self.preview_header_btn.configure(text="▼ Playlist Videos List (Click to Collapse)")
            self.is_preview_open = True
        else:
            self.playlist_preview_frame.pack_forget()
            self.preview_header_btn.configure(text="▶ Playlist Videos List (Click to Expand)")
            self.is_preview_open = False

    def change_font_size(self, choice):
        if "20" in choice:
            self.current_font_size = 20
            self.title_font_size = 28
        elif "22" in choice:
            self.current_font_size = 22
            self.title_font_size = 30
        else:
            self.current_font_size = 18
            self.title_font_size = 26

        self.title_label.configure(font=("Helvetica", self.title_font_size, "bold"))
        self.url_entry.configure(font=("Arial", self.current_font_size))
        self.folder_entry.configure(font=("Arial", self.current_font_size))
        self.fetch_btn.configure(font=("Arial", self.current_font_size, "bold"))
        self.quality_menu.configure(font=("Arial", self.current_font_size))

    def open_docs(self):
        DocumentationWindow(self)

    def on_path_selected(self, choice):
        if choice and choice != "Quick Paths ▼":
            self.folder_var.set(choice)
            self.folder_entry.configure(text_color=self.folder_entry.default_fg_color)

    def setup_placeholder(self, entry, placeholder_text):
        entry.placeholder = placeholder_text
        entry.placeholder_color = "gray"
        entry.default_fg_color = entry.cget("text_color")

        def on_focus_in(event):
            if entry.get() == entry.placeholder:
                entry.delete(0, "end")
                entry.configure(text_color=entry.default_fg_color)

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, entry.placeholder)
                entry.configure(text_color=entry.placeholder_color)

        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.configure(text_color=entry.placeholder_color)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def fetch_qualities(self):
        url = self.url_var.get().strip()
        if not url or url == self.url_entry.placeholder:
            messagebox.showerror("Error", "Please enter a valid URL first!")
            return
        
        is_playlist = self.is_playlist_url(url)
        self.fetch_btn.configure(state="disabled", text="Fetching...")
        
        def run():
            try:
                cmd = ["yt-dlp", "-J", url]
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, _ = process.communicate()
                
                data = json.loads(stdout)
                
                self.qualities_dict.clear()
                quality_list = []

                if is_playlist and data and "_type" in data and data["_type"] == "playlist":
                    self.playlist_entries = data.get("entries", [])
                    
                    for widget in self.playlist_scroll_frame.winfo_children():
                        widget.destroy()
                    self.video_checkboxes.clear()

                    for entry in self.playlist_entries:
                        if entry: # حماية ضد العناصر الفارغة NoneType
                            v_title = entry.get("title", "Unknown Title")
                            v_id = entry.get("id")
                            var = ctk.BooleanVar(value=True)
                            chk = ctk.CTkCheckBox(self.playlist_scroll_frame, text=v_title, variable=var, font=("Arial", 14))
                            chk.pack(anchor="w", pady=4)
                            self.video_checkboxes.append((v_id, var))

                    # إظهار زر البلايليست تلقائياً
                    self.after(0, lambda: self.preview_header_btn.pack(padx=30, anchor="w", pady=(8, 0)))

                    quality_list = ["Best Quality (Default)", "720p - mp4", "1080p - mp4"]
                    self.qualities_dict["Best Quality (Default)"] = "best"
                    self.qualities_dict["720p - mp4"] = "137"
                    self.qualities_dict["1080p - mp4"] = "137"
                else:
                    # إخفاء زر البلايليست لو كان فيديو فردي
                    self.after(0, lambda: self.preview_header_btn.pack_forget())
                    self.after(0, lambda: self.playlist_preview_frame.pack_forget())
                    self.is_preview_open = False

                    formats = data.get("formats", [])
                    for f in formats:
                        if f and f.get("vcodec") != "none" and f.get("height"):
                            resolution = f"{f['height']}p"
                            ext = f.get("ext", "mp4")
                            format_id = f["format_id"]
                            filesize = f.get("filesize") or f.get("filesize_approx")
                            size_str = f" ({size_format(filesize)})" if filesize else ""
                            
                            label = f"{resolution} - {ext}{size_str}"
                            self.qualities_dict[label] = format_id
                            if label not in quality_list:
                                quality_list.append(label)
                    
                    quality_list = sorted(quality_list, key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0, reverse=True)
                
                if quality_list:
                    self.quality_menu.configure(values=quality_list, state="normal")
                    self.quality_menu.set(quality_list[0])
                    self.status_label.configure(text="Data fetched successfully. Ready.")
                else:
                    self.status_label.configure(text="No valid formats found.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred:\n{e}")
            finally:
                self.fetch_btn.configure(state="normal", text="Fetch Data")

        threading.Thread(target=run).start()

    def start_download_thread(self):
        url = self.url_var.get().strip()
        path = self.folder_var.get().strip()
        selected_label = self.quality_menu.get()
        is_playlist = self.is_playlist_url(url)

        if not url or url == self.url_entry.placeholder:
            messagebox.showerror("Error", "Please enter a video/playlist URL!")
            return
        if not path or path == self.folder_entry.placeholder:
            messagebox.showerror("Error", "Please select a save folder!")
            return

        format_id = self.qualities_dict.get(selected_label, "best")
        
        self.download_btn.configure(state="disabled", text="Downloading...")
        self.progress_bar.set(0)

        threading.Thread(target=lambda: self.run_download(url, path, format_id, is_playlist)).start()

    def run_download(self, url, path, format_id, is_playlist):
        output_template = f"{path}/%(title)s.%(ext)s"
        
        cmd = [
            "yt-dlp",
            "-f", f"{format_id}+ba/b" if not is_playlist else "bv*+ba/b",
            "--merge-output-format", "mp4",
            "-o", output_template,
            "--newline",
            url
        ]

        if is_playlist and self.video_checkboxes:
            excluded_ids = [vid for vid, var in self.video_checkboxes if not var.get()]
            if excluded_ids:
                cmd.extend(["--match-filter", "id !=" + " & id !=".join(excluded_ids)])

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            if "%" in line:
                match = re.search(r'([\d.]+)%', line)
                if match:
                    try:
                        percentage = float(match.group(1)) / 100.0
                        self.progress_bar.set(percentage)
                    except:
                        pass
                self.after(0, lambda l=line.strip(): self.status_label.configure(text=l))

        process.wait()
        
        if process.returncode == 0:
            self.after(0, lambda: messagebox.showinfo("Success", "Download completed successfully!"))
            self.after(0, lambda: self.status_label.configure(text="Download completed."))
            self.progress_bar.set(1.0)
        else:
            self.after(0, lambda: messagebox.showerror("Error", "An error occurred during download."))
            self.after(0, lambda: self.status_label.configure(text="Download failed."))

        self.after(0, lambda: self.download_btn.configure(state="normal", text="Start Download"))

def size_format(b):
    if not b:
        return ""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if b < 1024.0:
            return f"{b:.1f} {unit}"
        b /= 1024.0
    return f"{b:.1f} TB"

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
