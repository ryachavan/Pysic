import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
import random
from pathlib import Path

# Node class for Doubly Circular Linked List
class SongNode:
    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path
        self.prev = None
        self.next = None

# Doubly Circular Linked List for Playlist
class DoublyCircularLinkedList:
    def __init__(self):
        self.head = None
        self.current = None
        self.size = 0
    
    def add(self, name, file_path):
        new_node = SongNode(name, file_path)
        
        if not self.head:
            self.head = new_node
            self.head.next = self.head
            self.head.prev = self.head
            self.current = self.head
        else:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node
        
        self.size += 1
        return new_node
    
    def remove(self, name):
        if not self.head:
            return False
        
        temp = self.head
        while True:
            if temp.name == name:
                if self.size == 1:
                    self.head = None
                    self.current = None
                else:
                    temp.prev.next = temp.next
                    temp.next.prev = temp.prev
                    
                    if temp == self.head:
                        self.head = temp.next
                    if temp == self.current:
                        self.current = temp.next
                
                self.size -= 1
                return True
            
            temp = temp.next
            if temp == self.head:
                break
        
        return False
    
    def next_song(self):
        if self.current:
            self.current = self.current.next
            return self.current
        return None
    
    def previous_song(self):
        if self.current:
            self.current = self.current.prev
            return self.current
        return None
    
    def get_current(self):
        return self.current
    
    def get_all(self):
        songs = []
        if not self.head:
            return songs
        
        temp = self.head
        while True:
            songs.append({'name': temp.name, 'path': temp.file_path})
            temp = temp.next
            if temp == self.head:
                break
        
        return songs
    
    def get_random_song(self):
        if self.size == 0:
            return None
        
        random_index = random.randint(0, self.size - 1)
        temp = self.head
        for _ in range(random_index):
            temp = temp.next
        
        self.current = temp
        return temp
    
    def find_song(self, name):
        if not self.head:
            return None
        
        temp = self.head
        while True:
            if temp.name == name:
                self.current = temp
                return temp
            temp = temp.next
            if temp == self.head:
                break
        return None

# Stack for Recently Played
class Stack:
    def __init__(self, max_size=10):
        self.items = []
        self.max_size = max_size
    
    def push(self, song):
        if len(self.items) >= self.max_size:
            self.items.pop(0)
        self.items.append(song)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def get_all(self):
        return list(reversed(self.items))
    
    def is_empty(self):
        return len(self.items) == 0

# Music Player Application
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Music Player - Data Structures")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a2e")
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Data structures
        self.playlist = DoublyCircularLinkedList()
        self.recently_played = Stack(10)
        
        # State variables
        self.is_playing = False
        self.is_paused = False
        self.is_shuffle = False
        self.current_song = None
        
        # Create UI
        self.create_widgets()
        
        # Start update loop
        self.update_progress()
    
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#1a1a2e")
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🎵 Music Player",
            font=("Arial", 28, "bold"),
            bg="#1a1a2e",
            fg="#e94560"
        )
        title_label.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Using Doubly Circular Linked List & Stack",
            font=("Arial", 10),
            bg="#1a1a2e",
            fg="#a0a0a0"
        )
        subtitle.pack()
        
        # Load Folder Button
        load_frame = tk.Frame(self.root, bg="#16213e", bd=2, relief=tk.RAISED)
        load_frame.pack(pady=10, padx=20, fill=tk.X)
        
        load_btn = tk.Button(
            load_frame,
            text="📁 Load Music Folder",
            command=self.load_folder,
            font=("Arial", 12, "bold"),
            bg="#e94560",
            fg="white",
            activebackground="#d63447",
            cursor="hand2",
            padx=20,
            pady=10
        )
        load_btn.pack(pady=10)
        
        # Current Song Display
        song_frame = tk.Frame(self.root, bg="#16213e", bd=2, relief=tk.RAISED)
        song_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.current_song_label = tk.Label(
            song_frame,
            text="No Song Selected",
            font=("Arial", 16, "bold"),
            bg="#16213e",
            fg="#f1f1f1",
            wraplength=800
        )
        self.current_song_label.pack(pady=10)
        
        self.mode_label = tk.Label(
            song_frame,
            text="Sequential Mode",
            font=("Arial", 10),
            bg="#16213e",
            fg="#a0a0a0"
        )
        self.mode_label.pack(pady=5)
        
        # Progress Bar
        progress_frame = tk.Frame(song_frame, bg="#16213e")
        progress_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.Scale(
            progress_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.progress_var,
            state=tk.DISABLED,  # Disable seeking to prevent audio issues
            bg="#16213e",
            fg="#f1f1f1",
            troughcolor="#0f3460",
            highlightthickness=0,
            showvalue=0
        )
        self.progress_bar.pack(fill=tk.X)
        
        time_frame = tk.Frame(song_frame, bg="#16213e")
        time_frame.pack(fill=tk.X, padx=20)
        
        self.current_time_label = tk.Label(
            time_frame,
            text="0:00",
            font=("Arial", 9),
            bg="#16213e",
            fg="#a0a0a0"
        )
        self.current_time_label.pack(side=tk.LEFT)
        
        self.total_time_label = tk.Label(
            time_frame,
            text="0:00",
            font=("Arial", 9),
            bg="#16213e",
            fg="#a0a0a0"
        )
        self.total_time_label.pack(side=tk.RIGHT)
        
        # Control Buttons
        control_frame = tk.Frame(self.root, bg="#16213e", bd=2, relief=tk.RAISED)
        control_frame.pack(pady=10, padx=20)
        
        button_style = {
            "font": ("Arial", 10, "bold"),
            "bg": "#0f3460",
            "fg": "white",
            "activebackground": "#16213e",
            "cursor": "hand2",
            "width": 10,
            "height": 2
        }
        
        btn_frame = tk.Frame(control_frame, bg="#16213e")
        btn_frame.pack(pady=15)
        
        self.shuffle_btn = tk.Button(
            btn_frame,
            text="🔀 Shuffle",
            command=self.toggle_shuffle,
            **button_style
        )
        self.shuffle_btn.grid(row=0, column=0, padx=5)
        
        prev_btn = tk.Button(
            btn_frame,
            text="⏮️ Previous",
            command=self.play_previous,
            **button_style
        )
        prev_btn.grid(row=0, column=1, padx=5)
        
        self.play_pause_btn = tk.Button(
            btn_frame,
            text="▶️ Play",
            command=self.toggle_play_pause,
            font=("Arial", 12, "bold"),
            bg="#e94560",
            fg="white",
            activebackground="#d63447",
            cursor="hand2",
            width=10,
            height=2
        )
        self.play_pause_btn.grid(row=0, column=2, padx=5)
        
        next_btn = tk.Button(
            btn_frame,
            text="⏭️ Next",
            command=self.play_next,
            **button_style
        )
        next_btn.grid(row=0, column=3, padx=5)
        
        stop_btn = tk.Button(
            btn_frame,
            text="⏹️ Stop",
            command=self.stop,
            **button_style
        )
        stop_btn.grid(row=0, column=4, padx=5)
        
        # Playlist and Recent Buttons
        list_frame = tk.Frame(control_frame, bg="#16213e")
        list_frame.pack(pady=10)
        
        playlist_btn = tk.Button(
            list_frame,
            text="📜 View Playlist",
            command=self.show_playlist,
            **button_style
        )
        playlist_btn.grid(row=0, column=0, padx=5)
        
        recent_btn = tk.Button(
            list_frame,
            text="🕒 Recently Played",
            command=self.show_recent,
            **button_style
        )
        recent_btn.grid(row=0, column=1, padx=5)
        
        # Info Section
        info_frame = tk.Frame(self.root, bg="#0f3460", bd=2, relief=tk.RAISED)
        info_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        info_label = tk.Label(
            info_frame,
            text="📚 Data Structures Used:",
            font=("Arial", 11, "bold"),
            bg="#0f3460",
            fg="#f1f1f1"
        )
        info_label.pack(anchor=tk.W, padx=10, pady=5)
        
        info_text = """
• Doubly Circular Linked List - Playlist management with bidirectional traversal
• Stack (LIFO) - Recently played songs tracking (max 10)
• Randomization - Shuffle mode with random song selection
        """
        
        info_content = tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg="#0f3460",
            fg="#a0a0a0",
            justify=tk.LEFT
        )
        info_content.pack(anchor=tk.W, padx=20, pady=5)
        
        self.stats_label = tk.Label(
            info_frame,
            text="Songs in Playlist: 0",
            font=("Arial", 10),
            bg="#0f3460",
            fg="#e94560"
        )
        self.stats_label.pack(pady=10)
    
    def load_folder(self):
        folder_path = filedialog.askdirectory(title="Select Music Folder")
        
        if not folder_path:
            return
        
        # Clear existing playlist
        self.playlist = DoublyCircularLinkedList()
        self.stop()
        
        # Load all MP3 files
        mp3_files = []
        for file in os.listdir(folder_path):
            if file.lower().endswith('.mp3'):
                mp3_files.append(file)
        
        if not mp3_files:
            messagebox.showwarning("No MP3 Files", "No MP3 files found in the selected folder!")
            return
        
        # Add to playlist
        for file in mp3_files:
            file_path = os.path.join(folder_path, file)
            song_name = os.path.splitext(file)[0]
            self.playlist.add(song_name, file_path)
        
        self.current_song = self.playlist.get_current()
        self.update_display()
        self.stats_label.config(text=f"Songs in Playlist: {self.playlist.size}")
        
        messagebox.showinfo("Success", f"Loaded {len(mp3_files)} MP3 files!")
    
    def play_song(self, song):
        if song:
            try:
                pygame.mixer.music.load(song.file_path)
                pygame.mixer.music.play()
                self.is_playing = True
                self.is_paused = False
                self.current_song = song
                self.recently_played.push({'name': song.name, 'path': song.file_path})
                self.update_display()
            except Exception as e:
                messagebox.showerror("Error", f"Could not play song: {str(e)}")
    
    def toggle_play_pause(self):
        if self.playlist.size == 0:
            messagebox.showwarning("No Songs", "Please load a folder with MP3 files first!")
            return
        
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_pause_btn.config(text="▶️ Play")
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_pause_btn.config(text="⏸️ Pause")
        else:
            song = self.playlist.get_current()
            self.play_song(song)
            self.play_pause_btn.config(text="⏸️ Pause")
    
    def play_next(self):
        if self.is_shuffle:
            song = self.playlist.get_random_song()
        else:
            song = self.playlist.next_song()
        
        if song:
            self.play_song(song)
            self.play_pause_btn.config(text="⏸️ Pause")
    
    def play_previous(self):
        song = self.playlist.previous_song()
        if song:
            self.play_song(song)
            self.play_pause_btn.config(text="⏸️ Pause")
    
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.play_pause_btn.config(text="▶️ Play")
        self.progress_var.set(0)
    
    def toggle_shuffle(self):
        self.is_shuffle = not self.is_shuffle
        if self.is_shuffle:
            self.shuffle_btn.config(bg="#e94560")
            self.mode_label.config(text="🔀 Shuffle Mode")
        else:
            self.shuffle_btn.config(bg="#0f3460")
            self.mode_label.config(text="📜 Sequential Mode")
    
    def seek(self, value):
        # Disable seeking to prevent audio breaking
        # Seeking in pygame.mixer.music can cause issues
        pass
    
    def update_progress(self):
        if self.is_playing and not self.is_paused:
            try:
                # Check if music is still playing
                if not pygame.mixer.music.get_busy():
                    # Song ended, play next
                    self.root.after(100, self.play_next)
                else:
                    # Update progress (visual only, no seeking)
                    if self.current_song and os.path.exists(self.current_song.file_path):
                        try:
                            song_length = pygame.mixer.Sound(self.current_song.file_path).get_length()
                            current_pos = pygame.mixer.music.get_pos() / 1000
                            
                            if song_length > 0 and current_pos >= 0:
                                progress = min((current_pos / song_length) * 100, 100)
                                self.progress_var.set(progress)
                                
                                self.current_time_label.config(text=self.format_time(current_pos))
                                self.total_time_label.config(text=self.format_time(song_length))
                        except Exception as e:
                            # If we can't get length, just show basic info
                            pass
            except Exception as e:
                pass
        
        self.root.after(1000, self.update_progress)
    
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02d}"
    
    def update_display(self):
        if self.current_song:
            self.current_song_label.config(text=self.current_song.name)
        else:
            self.current_song_label.config(text="No Song Selected")
    
    def show_playlist(self):
        playlist_window = tk.Toplevel(self.root)
        playlist_window.title("📜 Playlist")
        playlist_window.geometry("600x400")
        playlist_window.configure(bg="#1a1a2e")
        
        title = tk.Label(
            playlist_window,
            text=f"📜 Playlist ({self.playlist.size} songs)",
            font=("Arial", 14, "bold"),
            bg="#1a1a2e",
            fg="#e94560"
        )
        title.pack(pady=10)
        
        frame = tk.Frame(playlist_window, bg="#16213e")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 11),
            bg="#16213e",
            fg="#f1f1f1",
            selectbackground="#e94560",
            selectforeground="white",
            height=15
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        songs = self.playlist.get_all()
        for i, song in enumerate(songs, 1):
            status = "▶️ " if self.current_song and song['name'] == self.current_song.name else "   "
            listbox.insert(tk.END, f"{status}{i}. {song['name']}")
        
        def play_selected(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                song_name = songs[index]['name']
                song = self.playlist.find_song(song_name)
                if song:
                    self.play_song(song)
                    self.play_pause_btn.config(text="⏸️ Pause")
                    playlist_window.destroy()
        
        listbox.bind('<Double-Button-1>', play_selected)
        
        def remove_selected():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                song_name = songs[index]['name']
                if messagebox.askyesno("Remove Song", f"Remove '{song_name}' from playlist?"):
                    self.playlist.remove(song_name)
                    self.stats_label.config(text=f"Songs in Playlist: {self.playlist.size}")
                    playlist_window.destroy()
        
        remove_btn = tk.Button(
            playlist_window,
            text="🗑️ Remove Selected",
            command=remove_selected,
            font=("Arial", 10, "bold"),
            bg="#e94560",
            fg="white",
            cursor="hand2"
        )
        remove_btn.pack(pady=10)
    
    def show_recent(self):
        recent_window = tk.Toplevel(self.root)
        recent_window.title("🕒 Recently Played")
        recent_window.geometry("600x400")
        recent_window.configure(bg="#1a1a2e")
        
        title = tk.Label(
            recent_window,
            text="🕒 Recently Played (Stack - LIFO)",
            font=("Arial", 14, "bold"),
            bg="#1a1a2e",
            fg="#e94560"
        )
        title.pack(pady=10)
        
        frame = tk.Frame(recent_window, bg="#16213e")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(
            frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 11),
            bg="#16213e",
            fg="#f1f1f1",
            selectbackground="#e94560",
            selectforeground="white",
            height=15
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        recent_songs = self.recently_played.get_all()
        if recent_songs:
            for i, song in enumerate(recent_songs, 1):
                listbox.insert(tk.END, f"{i}. {song['name']}")
        else:
            listbox.insert(tk.END, "No recently played songs")

def main():
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()