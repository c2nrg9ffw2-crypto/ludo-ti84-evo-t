# Ludo for the TI-84 Evo-T

The board game **Ludo** (in German: *Mensch ärgere dich nicht*) for the **TI-84 Evo-T**
graphing calculator, written in Python. For 2 to 4 players. Empty seats can be played by the calculator.

> **Made with AI:** this game and this README were created with the help of AI (Claude by Anthropic).
> Everything was tested on a real TI-84 Evo-T.

## Features

- **2 to 4 players**: red, green, yellow and blue (2 players use red and yellow)
- **Computer players** for empty seats (marked with a **C**)
- A colourful board with yards, track, start squares and home lanes
- Pieces move square by square, so you can follow them
- Wins per colour stay saved after you quit

## Rules

- Everyone has **4 pieces** that start in their **yard** (the big coloured corner).
- Roll the die and move one piece that many squares along the white track.
- You need a **6** to bring a piece out of the yard onto your **start square**
  (the light-coloured square next to your yard).
- With **no pieces out**, you get **3 tries** to roll a 6.
- A **6** gives you **another roll**.
- **Land on someone** and their piece goes **back to their yard**!
- After going all the way round, your pieces go into your own **home lane**
  (the coloured lane pointing to the middle). You need the exact number to finish.
- Get all **4 pieces home** to win.

A **white dot** on a piece means 2 or more of your pieces are on that square.

## What you need

- A **TI-84 Evo-T** calculator
- A USB cable to connect it to your computer
- **Google Chrome** or **Microsoft Edge** (Safari and Firefox do not work with the TI tool)
- The file [`ludo.py`](ludo.py) from this repo

## Setup

1. Download [`ludo.py`](ludo.py) to your computer.
2. Connect the calculator to your computer with the USB cable.
   Leave the calculator on the **home screen**.
3. Open **https://connectevo.ti.com** in **Chrome** or **Edge**.
4. Connect to your calculator in the page and allow access when the browser asks.
5. Drag `ludo.py` onto the page to send it to the calculator.
6. **Choose RAM** to play right away.
   The Python app on the Evo-T only shows files that are in RAM.
   (Want to keep the game safe? See [Don't lose the game](#dont-lose-the-game).)

> **Already sent it to Archive?** On the **home screen** (not in the Python app) press **2nd → mem → Mem Management**,
> find **LUDO** and press **enter**. The `*` in front of the name disappears, which means
> it is now in RAM.

## Start the game

1. Open the **Python** app on the calculator.
2. Choose **LUDO** and run it.
3. Choose **2, 3 or 4 players** with ▲ ▼ and press **enter**.
4. Choose how many are the **calculator** ("All people", "1 computer" …).

## Keys

| Key | What it does |
|---|---|
| enter | Roll the die |
| ◀ ▶ | If more than one piece can move: choose one (blue frame) |
| enter | Move the chosen piece |
| clear | Quit |

If only one piece can move, it moves by itself.

## Don't lose the game

The Evo-T **deletes RAM** when it stays turned off for a while.
A normal turn-off is fine, but after some time the game is gone.

**Best way:**

1. Keep the game in **Archive**. Archive is never deleted.
2. Go to the **home screen**. If you are in the Python app, leave it with **2nd → quit**
   (quit is above the **mode** key). In the Python app, **2nd → mem** does nothing.
3. Press **2nd → mem** (mem is above the **+** key) and choose **2: Mem Management**.
4. Choose the list with Python programs (or **All**).
5. Find **LUDO** and press **enter**. The `*` disappears, which means the game is now in RAM.
6. Open the **Python** app and play.

Programs can't move files between Archive and RAM by themselves, so this step can't be automatic.
The wins list **LUDO** is in RAM too, so it can be deleted the same way.

## Wins

The wins of each colour are saved in a calculator list called **LUDO**, so they stay after you quit.
The start screen shows them.

- To reset them, delete the list **LUDO** in **2nd → mem → Mem Management** (on the home screen).
- A calculator reset (RAM clear) also resets them.

## Good to know

- Keep `ludo.py` on your computer too, so you can always send it again.
- Made for the TI-84 Evo-T. Other TI-84 models are not tested.
