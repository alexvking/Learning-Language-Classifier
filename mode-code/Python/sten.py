import sys
from PIL import Image
 
# Takes an image object and message string and returns a new image with the message encoded
def encode(image, message):
        # Extract the pixel data from the image into a list
        pixelData = list(image.tostring())
       
        # Append byte with message length to beginning of text to encode
        message = chr(len(message)) + message  
 
        # Iterate over each byte in the message and map each bit of least sig to bit of least sig of pixel data
        for i in range(len(message)):                          
                for j in range(8):
                        pixelData[i * 8 + j] = chr((ord(pixelData[i * 8 + j]) & 0xFE) | ((ord(message[i]) >> j) & 0x1))
       
        return Image.fromstring(image.mode, image.size, "".join(pixelData))
                       
 
# Takes a message object and returns the encoded string it contains                    
def decode(image):
        # List to hold final ASCII char values 
        message = []
       
        # Extract pixel data from the image into a list
        pixelData = list(image.tostring())
 
        # Get length of text from first eight bytes
        messageLength = 0x0;
       
        for i in range(8):
                messageLength = messageLength | ((ord(pixelData[i]) & 0x1) << i)
       
        # Iterate over length of message * 8 bytes and consolidate bits to obtain character code for each char in string
        for i in range(1, messageLength + 1):
                character = 0x0        
               
                for j in range(8):
                        character = character | ((ord(pixelData[i * 8 + j]) & 0x1) << j)
               
                message.append(chr(character))
 
        return "".join(message)
                       
 
def main():
        if (len(sys.argv) == 3):
                if (sys.argv[1] == "encode"):          
                        encode(Image.open(sys.argv[2]), raw_input("Enter message to encode (255 max length): ")).save(sys.argv[2][:sys.argv[2].index(".")] + "_encoded" + sys.argv[2][sys.argv[2].index("."):])
                        print("Encoding complete!")
                elif (sys.argv[1] == "decode"):
                        img = Image.open(sys.argv[2])
                        print("Message: " + decode(img))
        else:
                print("That thing you're doing... You're doing it wrong. Param format: <option> <image path>")
               
main()