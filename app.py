import tkinter as tk
import char_list as cl
import stats as st

# general info
root = tk.Tk()
root.title(" Morse App ")
root.geometry("650x450")

# root.resizable(0,0)

# some useful classes
class Message:
    # message class to hold messages        
    def __init__(self, row, column, message, colspan = 1, pos = root):
        self.label = tk.Label(pos, text=message, anchor="w")
        self.label.grid(column=column, row=row, columnspan = colspan, sticky=tk.EW, padx=8, pady=6)
        self.message = message
    def update_message(self, str):
        self.label.config(text = f"{self.message} {str}")

class Button:
    # class to make a button
    def __init__(self, row, column, text, command, pos = root):
        self.button = tk.Button(pos, text=text, command = command)
        self.button.grid(column=column, row=row, padx=8, pady=6, sticky=tk.EW)
    
class Textbox:
    # class to make a textbox
    def __init__(self, row, column, height, width, init_message, pos = root):
        self.textbox = tk.Text(pos, height=height, width=width)
        self.textbox.insert(0.,init_message)
        self.textbox.grid(column=column, row=row, padx=8, pady=6, sticky=tk.EW)

class Form:
    # combines textbox and button to make command executable form
    def __init__(self, row, init_message, init_text, command, pos = root):
        self.button = Button(row, 3, init_text, command, pos)
        self.text = Textbox(row, 4, 1, 20, init_message, pos)

class Options:
    def __init__(self, row, column, list, command, pos = root):
        self.list = list
        self.option_var = tk.IntVar()
        self.option_var.set(list[0])
        self.option = tk.OptionMenu(pos, self.option_var, *self.list, command = command)
        self.option.grid(column=column, row=row, sticky=tk.EW, padx=8, pady=6)

class Infobox:
    def __init__(self, row, column, height, width, text, pos = root):
        self.height = height
        self.width = width
        self.infolist = [[] for i in range(height)]
        for i in range(height):
            for j in range(width):
                self.infolist[i].append(Message(row+i,column+j,text[i][j],pos = pos))
    def update(self, text):
        for i in range(self.height):
            for j in range(self.width):
                self.infolist[i][j].update_message(text)

class Subpanel:
    def __init__(self, row, column, text, rowspan = 1, colspan = 1) :
        self.panel = tk.LabelFrame(root, text = text)
        self.panel.grid(row = row, column = column, rowspan = rowspan, columnspan = colspan, padx = 10, pady = 10, sticky=tk.EW)


def update_sound_params(form, min_len, max_len, cnt):
    try:
        INPUT = int(form.text.textbox.get("1.0", "end-1c"))
    except:
        error_message.update_message("Input is Not a Base 10 Integer")
    else:
        if (INPUT > max_len):
            error_message.update_message(f"Tone Length Too Large (>{max_len})")
            status_message.update_message("Update Unsuccessful...")
        elif (INPUT < min_len):
            error_message.update_message(f"Tone Length Too Short (<{min_len})")
            status_message.update_message("Update Unsuccessful...")
        else:
            cl.tone_len[cnt] = INPUT 
            # update_stats() 
            if (cnt != 2) :
                cl.play_len(INPUT)
            status_message.update_message("Update Successful!")

def guess_sound() :
    # INPUT = m_guess.text.textbox.get("1.0", "end-1c")
    INPUT = ""
    if (INPUT == "") :
        status_message.update_message("Please Insert a Guess...")
        return
    if (cl.guessed) :
        status_message.update_message("You've already guessed...")
        return
    if (INPUT == cl.last_word) :
        st.query(True)
        status_message.update_message("AC!")
    else :
        st.query(False)
        status_message.update_message("WA...")
    cl.guessed = True
    character_message.update_message(cl.last_word)


# def update_stats():
#     stats.config(text = f"Stats:\nTone Short: {cl.tone_len[0]}, Tone Long: {cl.tone_len[1]}, Tone Rest: {cl.tone_len[2]}")

# play = lambda: play_notes(3)
# button = tk.Button(root, text = "Test", command = play)
# button.grid(column = 0, row = 1)

def play_notes(num):
    for i in range(num):
        cl.play_26()

def update_char_type(x):
    cl.char_type = x 


stat_frame = Subpanel(0,0,"Status:").panel
setting_frame = Subpanel(0,1,"Settings:",1,3).panel
option_frame = Subpanel(1,1,"Options:",1,3).panel
message_frame = Subpanel(3,0,"Messages:",1,4).panel

# General Text Placement
Message(row = 0, column = 0, message = "Char Type:", pos = option_frame)
Message(row = 1, column = 0, message = "Rating Mode:", colspan=2, pos = option_frame)
# char_type = Options(0, 1, list = [26, 36, 10], command = lambda _:update_char_type(), pos = option_frame)
char_type = Options(0, 1, list = [26, 36, 10], command = lambda x:update_char_type(x), pos = option_frame)

Infobox(0, 0, 3, 1, [["Rating"],["Current Streak"],["Session Sum"]], stat_frame)
stats = Infobox(0, 1, 3, 2, [["Current:", "Max:"],["Current:","Max:"],["AC:","WA:"]], stat_frame)
setting = Infobox(1, 5, 3, 1, [[""],[""],[""]], pos = setting_frame)

m_short = Form(1, cl.tone_len[0], "Set Minimum Tone Length", lambda:update_sound_params(m_short,100,250,0), pos = setting_frame)
m_long = Form(2, cl.tone_len[1], "Set Maximum Tone Length", lambda:update_sound_params(m_long,250,1000,1), pos = setting_frame)
m_rest = Form(3, cl.tone_len[2], "Set Tone Rest Length", lambda:update_sound_params(m_rest,250,3000,2), pos = setting_frame)

character_message = Message(row = 7, column = 0, message = "Last Sounds:", colspan=6, pos = message_frame)
status_message = Message(row = 8, column= 0, message = "Status:", colspan=6, pos = message_frame)
error_message = Message(row = 9, column= 0, message = "Error Message:", colspan=6, pos = message_frame)





# m_guess = Form(8, "", "Guess!", lambda:guess_sound())

# stats = tk.Label(anchor = "w", justify="left")
# stats.grid(column=0, row = 11, columnspan= 10, rowspan=2)  



# update_stats()
root.mainloop()
