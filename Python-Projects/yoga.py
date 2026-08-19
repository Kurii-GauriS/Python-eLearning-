import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame


# ============================================================
# STRAY KIDS × YOGA — THIS & THAT AESTHETIC
# ============================================================

# --- PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MUSIC_FOLDER = "music"
POSE_IMAGE_FOLDER = os.path.join(BASE_DIR, "poses")


# ============================================================
# YOGA POSES
# ============================================================

YOGA_POSES = [
    ("Mountain Pose", "Tadasana", 120, "mountain.png"),
    ("Downward-Facing Dog", "Adho Mukha Svanasana", 150, "downward_dog.png"),
    ("Warrior I", "Virabhadrasana I", 150, "warrior1.png"),
    ("Tree Pose", "Vrksasana", 120, "tree.png"),
    ("Child's Pose", "Balasana", 120, "childs_pose.png"),
]


# ============================================================
# THIS & THAT × MINDFUL YOGA COLOR PALETTE
# ============================================================

COLOR_BG = "#E8F0EA"          # Soft sage background
COLOR_CARD = "#FFF9EF"        # Warm cream
COLOR_CARD_ALT = "#F4EBDD"    # Slightly deeper cream

COLOR_SEAFOAM = "#78BFA8"     # Main calming accent
COLOR_SEAFOAM_DARK = "#5FA58D"

COLOR_ORANGE = "#E8A15A"      # Soft THIS & THAT tangerine
COLOR_ORANGE_DARK = "#D47E35"

COLOR_TEXT = "#26332E"        # Deep green-black
COLOR_SUBTEXT = "#7A8580"     # Muted green-grey

COLOR_WHITE = "#FFFFFF"

FONT_MAIN = "Segoe UI"


# ============================================================
# MAIN APP
# ============================================================

class SKZYogaApp:

    def __init__(self, root):

        self.root = root

        self.root.title("SKZ • Mindful Flow")
        self.root.geometry("500x760")
        self.root.configure(bg=COLOR_BG)
        self.root.resizable(False, False)

        # ---------------------------
        # Audio
        # ---------------------------

        pygame.mixer.init()

        self.playlist = self.load_mp3_files()
        self.current_song_idx = 0

        # ---------------------------
        # Session
        # ---------------------------

        self.running = False
        self.current_pose_idx = 0
        self.time_left = 0
        self.timer_job = None

        self.current_img_tk = None

        # ---------------------------
        # UI
        # ---------------------------

        self.setup_ui()


    # ========================================================
    # LOAD MUSIC
    # ========================================================

    def load_mp3_files(self):

        if not os.path.exists(MUSIC_FOLDER):
            return []

        files = [
            os.path.join(MUSIC_FOLDER, file)
            for file in os.listdir(MUSIC_FOLDER)
            if file.lower().endswith(".mp3")
        ]

        files.sort()

        return files


    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            self.root,
            bg=COLOR_CARD,
            height=78
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        # Small SKZ-style decorative symbol

        logo = tk.Label(
            header,
            text="✦",
            font=(FONT_MAIN, 20, "bold"),
            bg=COLOR_CARD,
            fg=COLOR_ORANGE
        )

        logo.pack(side="left", padx=(28, 5))

        title_frame = tk.Frame(
            header,
            bg=COLOR_CARD
        )

        title_frame.pack(side="left")

        title = tk.Label(
            title_frame,
            text="MINDFUL FLOW",
            font=(FONT_MAIN, 17, "bold"),
            bg=COLOR_CARD,
            fg=COLOR_SEAFOAM
        )

        title.pack(anchor="w")

        subtitle = tk.Label(
            title_frame,
            text="STRAY KIDS • YOGA SESSION",
            font=(FONT_MAIN, 8, "bold"),
            bg=COLOR_CARD,
            fg=COLOR_SUBTEXT
        )

        subtitle.pack(anchor="w")


        # ----------------------------------------------------
        # MAIN CONTENT
        # ----------------------------------------------------

        main = tk.Frame(
            self.root,
            bg=COLOR_BG
        )

        main.pack(fill="both", expand=True, padx=18, pady=15)


        # ----------------------------------------------------
        # WELCOME CARD
        # ----------------------------------------------------

        self.card = tk.Frame(
            main,
            bg=COLOR_CARD
        )

        self.card.pack(fill="both", expand=True)


        # ----------------------------------------------------
        # SESSION LABEL
        # ----------------------------------------------------

        self.pose_label = tk.Label(
            self.card,
            text="Ready to Begin?",
            font=(FONT_MAIN, 18, "bold"),
            bg=COLOR_CARD,
            fg=COLOR_TEXT
        )

        self.pose_label.pack(pady=(18, 2))


        self.pose_subtitle = tk.Label(
            self.card,
            text="Take a breath • Find your balance",
            font=(FONT_MAIN, 10),
            bg=COLOR_CARD,
            fg=COLOR_SUBTEXT
        )

        self.pose_subtitle.pack()


        # ----------------------------------------------------
        # IMAGE AREA
        # ----------------------------------------------------

        self.image_container = tk.Frame(
            self.card,
            width=270,
            height=210,
            bg=COLOR_CARD
        )

        self.image_container.pack(pady=12)

        self.image_container.pack_propagate(False)

        self.image_label = tk.Label(
            self.image_container,
            bg=COLOR_CARD
        )

        self.image_label.pack(
            fill="both",
            expand=True
        )

        self.show_placeholder_image()


        # ----------------------------------------------------
        # TIMER
        # ----------------------------------------------------

        self.timer_label = tk.Label(
            self.card,
            text="--:--",
            font=(FONT_MAIN, 36, "bold"),
            bg=COLOR_CARD,
            fg=COLOR_SEAFOAM
        )

        self.timer_label.pack(pady=(2, 0))


        # ----------------------------------------------------
        # PROGRESS BAR
        # ----------------------------------------------------

        progress_bg = tk.Frame(
            self.card,
            bg=COLOR_CARD_ALT,
            height=7
        )

        progress_bg.pack(
            fill="x",
            padx=45,
            pady=(6, 10)
        )

        progress_bg.pack_propagate(False)

        self.progress_fill = tk.Frame(
            progress_bg,
            bg=COLOR_SEAFOAM,
            height=7
        )

        self.progress_fill.place(
            x=0,
            y=0,
            relheight=1,
            relwidth=0
        )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status_label = tk.Label(
            self.card,
            text="Your little moment of calm starts here.",
            font=(FONT_MAIN, 10, "italic"),
            bg=COLOR_CARD,
            fg=COLOR_SUBTEXT
        )

        self.status_label.pack(pady=(0, 10))


        # ----------------------------------------------------
        # START BUTTON
        # ----------------------------------------------------

        self.start_button = tk.Button(
            self.card,
            text="START SESSION",
            font=(FONT_MAIN, 10, "bold"),
            bg=COLOR_ORANGE,
            fg=COLOR_WHITE,
            activebackground=COLOR_ORANGE_DARK,
            activeforeground=COLOR_WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=30,
            pady=11,
            command=self.toggle_session
        )

        self.start_button.pack(pady=(0, 18))


        # ----------------------------------------------------
        # SESSION INFO
        # ----------------------------------------------------

        self.session_info = tk.Label(
            self.card,
            text="5 poses • 10 minutes",
            font=(FONT_MAIN, 9, "bold"),
            bg=COLOR_CARD,
            fg=COLOR_SUBTEXT
        )

        self.session_info.pack(
            pady=(0, 15)
        )


        # ----------------------------------------------------
        # MUSIC CARD
        # ----------------------------------------------------

        music_card = tk.Frame(
            main,
            bg=COLOR_CARD
        )

        music_card.pack(
            fill="x",
            pady=(12, 0)
        )


        music_title = tk.Label(
            music_card,
            text="♫  SKZ SOUNDTRACK",
            font=(FONT_MAIN, 9, "bold"),
            bg=COLOR_CARD,
            fg=COLOR_SEAFOAM
        )

        music_title.pack(pady=(10, 3))


        self.song_label = tk.Label(
            music_card,
            text=self.get_current_song_name(),
            font=(FONT_MAIN, 9),
            bg=COLOR_CARD,
            fg=COLOR_SUBTEXT
        )

        self.song_label.pack(
            padx=15,
            pady=(0, 7)
        )


        # ----------------------------------------------------
        # MUSIC BUTTONS
        # ----------------------------------------------------

        btn_frame = tk.Frame(
            music_card,
            bg=COLOR_CARD
        )

        btn_frame.pack(
            pady=(0, 12)
        )


        button_style = {
            "font": (FONT_MAIN, 9, "bold"),
            "bg": COLOR_BG,
            "fg": COLOR_TEXT,
            "activebackground": COLOR_SEAFOAM,
            "activeforeground": COLOR_WHITE,
            "relief": "flat",
            "bd": 0,
            "cursor": "hand2",
            "width": 8,
            "pady": 5
        }


        tk.Button(
            btn_frame,
            text="◀ PREV",
            command=self.prev_song,
            **button_style
        ).grid(
            row=0,
            column=0,
            padx=3
        )


        self.play_btn = tk.Button(
            btn_frame,
            text="▶ PLAY",
            command=self.toggle_music,
            bg=COLOR_ORANGE,
            fg=COLOR_WHITE,
            activebackground=COLOR_ORANGE_DARK,
            activeforeground=COLOR_WHITE,
            font=(FONT_MAIN, 9, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            width=8,
            pady=5
        )

        self.play_btn.grid(
            row=0,
            column=1,
            padx=3
        )


        tk.Button(
            btn_frame,
            text="NEXT ▶",
            command=self.next_song,
            **button_style
        ).grid(
            row=0,
            column=2,
            padx=3
        )


    # ========================================================
    # IMAGE HANDLING
    # ========================================================

    def load_pose_image(self, filename):

        image_path = os.path.join(
            POSE_IMAGE_FOLDER,
            filename
        )

        if os.path.exists(image_path):

            try:

                img = Image.open(image_path)

                img.thumbnail(
                    (250, 190),
                    Image.Resampling.LANCZOS
                )

                self.current_img_tk = ImageTk.PhotoImage(img)

                self.image_label.config(
                    image=self.current_img_tk,
                    text=""
                )

                return

            except Exception as error:

                print(
                    f"Error loading image {image_path}: {error}"
                )

        self.show_placeholder_image(
            "🧘"
        )


    def show_placeholder_image(self, text="🧘"):

        self.image_label.config(
            image="",
            text=text,
            font=(FONT_MAIN, 46),
            fg=COLOR_ORANGE,
            bg=COLOR_CARD
        )


    # ========================================================
    # SESSION
    # ========================================================

    def toggle_session(self):

        if not self.running:

            self.running = True

            self.current_pose_idx = 0

            self.start_button.config(
                text="STOP SESSION",
                bg=COLOR_SEAFOAM_DARK
            )

            self.start_pose()

            # Start music automatically

            if self.playlist:

                if not pygame.mixer.music.get_busy():

                    self.play_music()

        else:

            self.reset_session()


    def start_pose(self):

        if not self.running:
            return

        if self.current_pose_idx < len(YOGA_POSES):

            (
                pose_name,
                sanskrit_name,
                duration,
                img_file
            ) = YOGA_POSES[self.current_pose_idx]


            # ----------------------------------------------
            # Pose title
            # ----------------------------------------------

            self.pose_label.config(
                text=pose_name
            )


            self.pose_subtitle.config(
                text=sanskrit_name
            )


            # ----------------------------------------------
            # Status
            # ----------------------------------------------

            self.status_label.config(
                text=f"Pose {self.current_pose_idx + 1} of {len(YOGA_POSES)}"
            )


            # ----------------------------------------------
            # Image
            # ----------------------------------------------

            self.load_pose_image(
                img_file
            )


            # ----------------------------------------------
            # Timer
            # ----------------------------------------------

            self.time_left = duration

            self.update_timer()

        else:

            self.complete_session()


    # ========================================================
    # TIMER
    # ========================================================

    def update_timer(self):

        if not self.running:
            return

        if self.time_left > 0:

            minutes, seconds = divmod(
                self.time_left,
                60
            )

            self.timer_label.config(
                text=f"{minutes:02d}:{seconds:02d}"
            )


            # ----------------------------------------------
            # Progress
            # ----------------------------------------------

            duration = YOGA_POSES[
                self.current_pose_idx
            ][2]

            progress = (
                duration - self.time_left
            ) / duration

            self.progress_fill.place(
                relwidth=progress
            )


            self.time_left -= 1


            self.timer_job = self.root.after(
                1000,
                self.update_timer
            )

        else:

            self.current_pose_idx += 1

            self.progress_fill.place(
                relwidth=0
            )

            self.start_pose()


    # ========================================================
    # RESET SESSION
    # ========================================================

    def reset_session(self):

        self.running = False


        if self.timer_job:

            self.root.after_cancel(
                self.timer_job
            )

            self.timer_job = None


        self.start_button.config(
            text="START SESSION",
            bg=COLOR_ORANGE
        )


        self.pose_label.config(
            text="Session Stopped"
        )


        self.pose_subtitle.config(
            text="Ready whenever you are."
        )


        self.timer_label.config(
            text="--:--"
        )


        self.status_label.config(
            text="Press start to begin your session"
        )


        self.progress_fill.place(
            relwidth=0
        )


        self.show_placeholder_image()


        pygame.mixer.music.stop()

        self.play_btn.config(
            text="▶ PLAY"
        )


    # ========================================================
    # SESSION COMPLETE
    # ========================================================

    def complete_session(self):

        self.running = False

        self.start_button.config(
            text="START SESSION",
            bg=COLOR_ORANGE
        )


        self.pose_label.config(
            text="Namaste 🙏"
        )


        self.pose_subtitle.config(
            text="You made time for yourself today."
        )


        self.timer_label.config(
            text="00:00"
        )


        self.status_label.config(
            text="Session completed successfully ✦"
        )


        self.progress_fill.place(
            relwidth=1
        )


        self.show_placeholder_image(
            "✦"
        )


        messagebox.showinfo(
            "Mindful Flow",
            "Your yoga practice is complete! 🧘\n\n"
            "Take a moment to breathe and enjoy the rest of your day."
        )


    # ========================================================
    # MUSIC
    # ========================================================

    def get_current_song_name(self):

        if not self.playlist:

            return "♫ No MP3 files found"

        filename = os.path.basename(
            self.playlist[
                self.current_song_idx
            ]
        )

        # Remove .mp3

        filename = os.path.splitext(
            filename
        )[0]

        return f"♫ {filename[:38]}"


    def play_music(self):

        if not self.playlist:
            return

        try:

            pygame.mixer.music.load(
                self.playlist[
                    self.current_song_idx
                ]
            )

            pygame.mixer.music.play()

            self.play_btn.config(
                text="⏸ PAUSE"
            )

            self.song_label.config(
                text=self.get_current_song_name()
            )

        except Exception as error:

            print(
                "Playback Error:",
                error
            )


    def toggle_music(self):

        if not self.playlist:
            return


        if pygame.mixer.music.get_busy():

            pygame.mixer.music.pause()

            self.play_btn.config(
                text="▶ PLAY"
            )

        else:

            self.play_music()


    def next_song(self):

        if not self.playlist:
            return

        self.current_song_idx = (
            self.current_song_idx + 1
        ) % len(self.playlist)

        self.play_music()


    def prev_song(self):

        if not self.playlist:
            return

        self.current_song_idx = (
            self.current_song_idx - 1
        ) % len(self.playlist)

        self.play_music()


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SKZYogaApp(root)

    root.mainloop()