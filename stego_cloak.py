from PIL import Image
import os

class SteganographyEngine:
    def __init__(self):
        self.delimiter = "*****" # Signal to stop reading

    def generate_data(self, data):
        """Convert string data into binary format."""
        new_data = []
        for i in data:
            new_data.append(format(ord(i), '08b'))
        return new_data

    def modify_pixels(self, pix, data):
        """Embed the binary data into the pixels."""
        data_list = self.generate_data(data)
        len_data = len(data_list)
        imdata = iter(pix)

        for i in range(len_data):
            # Extract 3 pixels at a time (R, G, B)
            pix = [value for value in next(imdata)[:3] +
                                next(imdata)[:3] +
                                next(imdata)[:3]]

            # Pixel value should be made odd for 1 and even for 0
            for j in range(0, 8):
                if (data_list[i][j] == '0') and (pix[j] % 2 != 0):
                    pix[j] -= 1
                elif (data_list[i][j] == '1') and (pix[j] % 2 == 0):
                    if pix[j] != 0:
                        pix[j] -= 1
                    else:
                        pix[j] += 1
            
            # The 8th pixel determines if we keep reading or stop
            if (i == len_data - 1):
                if (pix[-1] % 2 == 0):
                    if pix[-1] != 0:
                        pix[-1] -= 1
                    else:
                        pix[-1] += 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode(self):
        img_name = input("Enter image name (with extension, e.g., cover.png): ")
        if not os.path.exists(img_name):
            print(f"[!] Error: {img_name} not found.")
            return
            
        image = Image.open(img_name, 'r')
        data = input("Enter secret message to hide: ")
        if (len(data) == 0):
            raise ValueError('Data is empty')

        new_img = image.copy()
        # Encode the data + delimiter
        self.encode_enc(new_img, data + self.delimiter)

        new_name = input("Enter output filename (e.g., secret.png): ")
        new_img.save(new_name, str(new_name.split(".")[1].upper()))
        print(f"[+] SUCCESS: Message hidden in {new_name}")

    def encode_enc(self, new_img, data):
        w = new_img.size[0]
        (x, y) = (0, 0)
        
        for pixel in self.modify_pixels(new_img.getdata(), data):
            # Putting modified pixels in the new image
            new_img.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def decode(self):
        img_name = input("Enter image name to decode (e.g., secret.png): ")
        if not os.path.exists(img_name):
            print(f"[!] Error: {img_name} not found.")
            return

        image = Image.open(img_name, 'r')
        data = ''
        img_data = iter(image.getdata())

        while (True):
            pixels = [value for value in next(img_data)[:3] +
                                next(img_data)[:3] +
                                next(img_data)[:3]]

            binstr = ''
            for i in pixels[:8]:
                if (i % 2 == 0):
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if (pixels[-1] % 2 != 0):
                return data

# --- MAIN MENU ---
if __name__ == '__main__':
    stego = SteganographyEngine()
    print("--- GHOST WRITER: IMAGE STEGANOGRAPHY ---")
    print("1. Encode (Hide Message)")
    print("2. Decode (Read Message)")
    
    choice = input("Select Operation (1/2): ")
    if choice == '1':
        stego.encode()
    elif choice == '2':
        res = stego.decode()
        if res:
            # Clean up the delimiter
            print(f"\n[+] DECODED MESSAGE: {res.split('*****')[0]}")
        else:
            print("[-] No hidden message found.")
    else:
        print("Invalid Selection.")
