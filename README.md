# Ghost Writer: LSB Steganography Tool 🕵️‍♂️

A cryptographic tool that implements **Least Significant Bit (LSB)** steganography to conceal text payloads within PNG images.

## 🧠 Theory
Digital images are made of pixels, each with Red, Green, and Blue values (0-255).
* Binary of 255: `11111111`
* Binary of 254: `11111110`

The difference between these two colors is imperceptible to the human eye. This tool replaces the **last bit** (the LSB) of the pixel data with the bits of your secret message.

## 🛠️ Features
* **Encodes** ASCII text into standard PNG images.
* **Decodes** hidden messages from carrier images.
* **Zero-Loss:** Uses PNG (lossless compression) to ensure data integrity (JPEG compression would destroy the message).

## 🚀 Usage
1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Tool:**
    ```bash
    python stego_cloak.py
    ```
3.  **Operations:**
    * Select **1** to hide a message. You need a source image (e.g., `cover.png`).
    * Select **2** to reveal a message from a modified image.
