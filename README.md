# 🎵 Pysic - Music Player Built With Data Structures

Pysic is a desktop music player built using **Python**, **Tkinter**, and **Pygame**, but the real star here is the **custom data structure architecture** that powers the playlist and playback system.

This project intentionally avoids built‑in list shortcuts and instead implements its own **Circular Doubly Linked List** and **Stack** to demonstrate how real‑world software can be driven by fundamental data structures.

---

## 🔧 Features

- Load and play `.mp3` files from any folder
- Next/Previous navigation using CDLL traversal
- Shuffle mode with random access
- Pause, resume, stop controls
- Recently Played list managed by a stack
- Playlist viewer with remove‑song functionality
- Clean and interactive Tkinter GUI

---

## 🧠 Core Data Structures

### SongNode Structure
Each entry in the Circular Doubly Linked List is represented by a SongNode. It stores:

- `name` - the song's title (derived from filename)
- `file_path` - the full path to the mp3 file
- `prev` - pointer to the previous SongNode
- `next` - pointer to the next SongNode

This node structure is the backbone of the playlist system, enabling bidirectional and circular traversal.


Pysic is built around two custom‑implemented structures:

### **1. Circular Doubly Linked List (CDLL) - Playlist Management**

This structure stores the playlist in a circular loop, enabling infinite navigation in both directions.

**Why CDLL?**

- Lets the player go **next** and **previous** smoothly
- No need to handle index boundaries manually
- Every node has **prev** and **next**, forming a perfect loop

**Used for:**

- Maintaining the playlist
- Keeping track of the currently active song
- Sequential mode navigation

**Key Operations:**

- `add(name, path)` – Inserts song nodes
- `remove(name)` – Unlinks nodes safely
- `next_song()` / `previous_song()` – Circular traversal
- `get_random_song()` – Shuffle mode random access
- `find_song(name)` – Search inside the loop

---

### **2. Stack (LIFO) Recently Played Tracker (Hybrid Stack Implementation)**

Works exactly like a real‑world **history stack**.

**Why a Hybrid Stack?** A pure stack only allows removing the top element, which doesn't fit a full recently-played history display. This project uses a hybrid approach: a stack-like behavior for pushes but allows reading the entire structure without popping anything.

Used for:

- Tracking history
- Displaying all recent songs without destructive pops

Key Operations:

- `push(song)` – Adds a song to history
- `pop()` – Removes the last played
- `get_all()` – Returns items in LIFO order

---

## 📂 Project Structure

```
pysic/
│── app.py          # Main application
│── README.md       # You are reading this
```

---

## ▶️ Running the App

### **1. Install Dependencies**

```
pip install pygame
```

Tkinter ships with Python on most systems.

### **2. Run the Program**

```
python app.py
```

### **3. Load Music**

Click **Load Music Folder** and select a directory containing `.mp3` files.

You're ready to go.

---

## 📐 Data Structure Flow

```
        +-----------------------+
        | Circular Doubly       |
        | Linked List (CDLL)    |
        |  - Playlist           |
        +-----------+-----------+
                    |
                    v
         +--------------------+
         | Current Song Node  |
         +--------------------+
                    |
                    v
       +-------------------------+
       | Stack (Recently Played) |
       +-------------------------+
```

---

## 🎯 Why This Project Matters

This isn’t just another MP3 player. It’s a demonstration of:

- How **custom data structures** fit into real applications
- How GUI interaction maps to node‑level operations
- How playlist engines work under the hood

Perfect for students and developers exploring:

- DSA in real applications
- Tkinter GUI development
- File handling and media frameworks

---

## 💡 Future Enhancements

- Volume control
- Progress bar seeking
- Queue system
- Favorites

Feel free to contribute or fork!
