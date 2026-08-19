import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame

# --- CONFIGURATION ---
MUSIC_FOLDER = "."

# Each pose now includes: ("Pose Name", Duration in seconds, "image_filename.png")
YOGA_POSES = [
    ("Mountain Pose (Tadasana)", 10, "mountain.png"),
    ("Downward-Facing Dog (Adho Mukha Svanasana)", 15, "downward_dog.png"),
    ("Warrior I (Virabhadrasana I)", 15, "warrior1.png"),
    ("Tree Pose (Vrksasana)", 10, "tree.png"),
    ("Child's Pose (Balasana)", 20, "childs_pose.png")
]

# Aesthetic Palette
COLOR_BG = "#F4F6F0"
COLOR_CARD = "#FFFFFF"
COLOR_PRIMARY = "#5B7065"
COLOR_ACCENT = "#889C8C"
COLOR_TEXT = "#2C3E35"
COLOR_SUBTEXT = "#6C7A72"
COLOR_BTN = "#7A8F82"
COLOR_BTN_HOVER = "#667A6D"

FONT_MAIN = "Segoe UI"

class AestheticYogaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mindful Flow Yoga")
        self.root.geometry("480x680")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        pygame.mixer.init()
        self.playlist = self.load_mp3_files()
        self.current_song_idx = 0

        self.running = False
        self.current_pose_idx = 0
        self.time_left = 0
        self.current_img_tk = None

        self.setup_ui()

    def load_mp3_files(self):
        if not os.path.exists(MUSIC_FOLDER):
            return []
        files = [os.path.join(MUSIC_FOLDER, f) for f in os.listdir(MUSIC_FOLDER) if f.lower().endswith(".mp3")]
        files.sort()
        return files

    def setup_ui(self):
        # Header Banner
        header = tk.Frame(self.root, bg=COLOR_PRIMARY, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_lbl = tk.Label(
            header, text="❖  MINDFUL FLOW", font=(FONT_MAIN, 15, "bold"),
            bg=COLOR_PRIMARY, fg="#FFFFFF"
        )
        title_lbl.pack(expand=True)

        # Main Card
        card = tk.Frame(self.root, bg=COLOR_CARD, bd=0, highlightthickness=1, highlightbackground="#E0E4DC")
        card.pack(fill="both", expand=True, padx=25, pady=15)

        self.pose_label = tk.Label(
            card, text="Ready to Begin?", font=(FONT_MAIN, 14, "bold"),
            bg=COLOR_CARD, fg=COLOR_TEXT, wraplength=380, justify="center"
        )
        self.pose_label.pack(pady=(15, 5))

        # Image Container
        self.image_label = tk.Label(card, bg=COLOR_CARD)
        self.image_label.pack(pady=10)
        self.show_placeholder_image()

        self.timer_label = tk.Label(
            card, text="--:--", font=(FONT_MAIN, 32, "bold"),
            bg=COLOR_CARD, fg=COLOR_PRIMARY
        )
        self.timer_label.pack(pady=5)

        self.status_label = tk.Label(
            card, text="Press start to begin your session", font=(FONT_MAIN, 10, "italic"),
            bg=COLOR_CARD, fg=COLOR_SUBTEXT
        )
        self.status_label.pack(pady=(0, 10))

        # Main Action Button
        self.start_button = tk.Button(
            card, text="START SESSION", font=(FONT_MAIN, 10, "bold"),
            bg=COLOR_BTN, fg="white", activebackground=COLOR_BTN_HOVER, activeforeground="white",
            relief="flat", cursor="hand2", padx=20, pady=6, command=self.toggle_session
        )
        self.start_button.pack(pady=10)

        # Music Controls Frame
        music_card = tk.Frame(self.root, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#E0E4DC")
        music_card.pack(fill="x", padx=25, pady=(0, 15))

        self.song_label = tk.Label(
            music_card, text=self.get_current_song_name(), font=(FONT_MAIN, 9),
            bg=COLOR_CARD, fg=COLOR_SUBTEXT
        )
        self.song_label.pack(pady=(8, 4))

        btn_frame = tk.Frame(music_card, bg=COLOR_CARD)
        btn_frame.pack(pady=(0, 8))

        btn_style = {
            "font": (FONT_MAIN, 9), "bg": COLOR_BG, "fg": COLOR_TEXT,
            "activebackground": COLOR_ACCENT, "activeforeground": "white",
            "relief": "flat", "width": 7, "cursor": "hand2"
        }

        tk.Button(btn_frame, text="⏮ Prev", command=self.prev_song, **btn_style).grid(row=0, column=0, padx=3)
        self.play_btn = tk.Button(btn_frame, text="▶ Play", command=self.toggle_music, **btn_style)
        self.play_btn.grid(row=0, column=1, padx=3)
        tk.Button(btn_frame, text="Next ⏭", command=self.next_song, **btn_style).grid(row=0, column=2, padx=3)

    # --- IMAGE HELPERS ---
    def load_pose_image(self, filename):
        if os.path.exists(filename):
            try:
                img = Image.open(filename)
                img = img.resize((220, 180), Image.Resampling.LANCZOS)
                self.current_img_tk = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.current_img_tk, text="")
                return
            except Exception as e:
                print(f"Error loading image {filename}: {e}")
        
        self.show_placeholder_image(text="[ No Image Found ]")

    def show_placeholder_image(self, text="🧘"):
        self.image_label.config(
            image="", text=text, font=(FONT_MAIN, 40),
            fg=COLOR_ACCENT, bg=COLOR_CARD, width=12, height=3
        )

    # --- SESSION CONTROL ---
    def toggle_session(self):
        if not self.running:
            self.running = True
            self.current_pose_idx = 0
            self.start_button.config(text="STOP SESSION", bg="#C86D61")
            self.start_pose()
            if self.playlist and not pygame.mixer.music.get_busy():
                self.play_music()
        else:
            self.reset_session()

    def start_pose(self):
        if not self.running:
            return

        if self.current_pose_idx < len(YOGA_POSES):
            pose_name, duration, img_file = YOGA_POSES[self.current_pose_idx]
            self.pose_label.config(text=pose_name)
            self.status_label.config(text=f"Pose {self.current_pose_idx + 1} of {len(YOGA_POSES)}")
            self.load_pose_image(img_file)

            self.time_left = duration
            self.update_timer()
        else:
            self.complete_session()

    def update_timer(self):
        if not self.running:
            return

        if self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.current_pose_idx += 1
            self.start_pose()

    def reset_session(self):
        self.running = False
        self.start_button.config(text="START SESSION", bg=COLOR_BTN)
        self.pose_label.config(text="Session Stopped")
        self.timer_label.config(text="--:--")
        self.status_label.config(text="Press start to begin your session")
        self.show_placeholder_image()
        pygame.mixer.music.stop()
        self.play_btn.config(text="▶ Play")

    def complete_session(self):
        self.running = False
        self.start_button.config(text="START SESSION", bg=COLOR_BTN)
        self.pose_label.config(text="Namaste 🙏")
        self.timer_label.config(text="00:00")
        self.status_label.config(text="Session completed successfully")
        self.show_placeholder_image("✨")
        messagebox.showinfo("Mindful Flow", "Your yoga practice is complete!")

    # --- AUDIO LOGIC ---
    def get_current_song_name(self):
        if not self.playlist:
            return "♫ No MP3 files found in folder"
        filename = os.path.basename(self.playlist[self.current_song_idx])
        return f"♫ {filename[:35]}"

    def play_music(self):
        if not self.playlist:
            return
        try:
            pygame.mixer.music.load(self.playlist[self.current_song_idx])
            pygame.mixer.music.play()
            self.play_btn.config(text="⏸ Pause")
            self.song_label.config(text=self.get_current_song_name())
        except Exception as e:
            print("Playback Error:", e)

    def toggle_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.play_btn.config(text="▶ Play")
        else:
            if pygame.mixer.music.get_pos() > 0:
                pygame.mixer.music.unpause()
            else:
                self.play_music()
            self.play_btn.config(text="⏸ Pause")

    def next_song(self):
        if not self.playlist:
            return
        self.current_song_idx = (self.current_song_idx + 1) % len(self.playlist)
        self.play_music()

    def prev_song(self):
        if not self.playlist:
            return
        self.current_song_idx = (self.current_song_idx - 1) % len(self.playlist)
        self.play_music()


if __name__ == "__main__":
    root = tk.Tk()
    app = AestheticYogaApp(root)
    root.mainloop()