import tkinter as tk
import char_list as cl
import stats as st


# general info
root = tk.Tk()
root.title(" Morse App ")
root.resizable(0,0)


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
    def __init__(self, row, column, height, width, init_message, colspan = 1, pos = root):
        self.textbox = tk.Text(pos, height=height, width=width)
        self.textbox.insert(0.,init_message)
        self.textbox.grid(column=column, row=row, columnspan=colspan, padx=8, pady=6, sticky=tk.EW)

class Form:
    # combines textbox and button to make command executable form
    def __init__(self, row, init_message, init_text, command, pos = root):
        self.button = Button(row, 3, init_text, command, pos=pos)
        self.text = Textbox(row, 4, 1, 5, init_message, pos=pos)

class Options:
    def __init__(self, row, column, list, command, pos = root):
        self.list = list
        self.option_var = tk.IntVar()
        self.option_var.set(list[-1])
        self.option = tk.OptionMenu(pos, self.option_var, *self.list, command = command)
        self.option.grid(column=column, row=row, sticky=tk.EW, padx=8, pady=6)

class Radio_Button:
    def __init__(self, row, column, text, value, command, pos = root):
        self.var = rating_mode_var
        self.button = tk.Radiobutton(pos, text=text, variable=self.var, value=value, command=command)
        self.button.grid(column=column, row=row, sticky=tk.EW, padx=8, pady=6)

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
                self.infolist[i][j].update_message(text[i][j])

class Subpanel:
    def __init__(self, row, column, text, rowspan = 1, colspan = 1, pos = root) :
        self.panel = tk.LabelFrame(pos, text = text)
        self.panel.grid(row = row, column = column, rowspan = rowspan, columnspan = colspan, padx = 10, pady = 10, sticky=tk.EW)


def update_sound_params(form, min_len, max_len, cnt):
    try:
        INPUT = int(form.text.textbox.get("1.0", "end-1c"))
    except:
        error_message.update_message("Input is Not a Base 10 Integer")
        status_message.update_message("Update Unsuccessful...")
    else:
        if (INPUT > max_len):
            error_message.update_message(f"Tone Length Too Large (>{max_len})")
            status_message.update_message("Update Unsuccessful...")
        elif (INPUT < min_len):
            error_message.update_message(f"Tone Length Too Short (<{min_len})")
            status_message.update_message("Update Unsuccessful...")
        else:
            cl.tone_len[cnt] = INPUT 
            update_setting() 
            if (cnt != 2) :
                cl.play_len(INPUT)
            status_message.update_message("Update Successful!")

def guess_sound() :
    INPUT = m_guess.textbox.get("1.0", "end-1c")
    INPUT = INPUT.replace(" ","").upper()
    if (INPUT == "") :
        status_message.update_message("Please Insert a Guess...")
        return
    if (cl.guessed) :
        status_message.update_message("You've already guessed...")
        return
    # print(INPUT)
    # print(cl.last_word[0])
    if (INPUT == cl.last_word[0]) :
        st.query(True, cl.rating_mode == 1)
        status_message.update_message("AC!")
    else :
        st.query(False, cl.rating_mode == 1)
        status_message.update_message("WA...")
    cl.guessed = True
    character_message.update_message(cl.last_word[0])
    update_status()

def guess_game() :
    try:
        INPUT = int(m_char_len.textbox.get("1.0", "end-1c"))
        if (INPUT == 0) :
            return
    except:
        error_message.update_message("Input is Not a Base 10 Integer")
    else :
        if (cl.guessed == False) :
            st.query(False, cl.rating_mode == 1)
            update_status()
            character_message.update_message(cl.last_word[0])
        if (rating_mode_var == 0) :
            status_message.update_message("NOTE: RATED GUESS MODE")
        else :
            status_message.update_message("NOTE: Unrated guess mode")
        m_guess.textbox.delete('1.0',tk.END)
        cl.guessed = False 
        cl.create_and_play_word(INPUT)

def play_sound():
    INPUT = m_guess.textbox.get("1.0", "end-1c")
    if (INPUT == "") :
        status_message.update_message("Please Insert a Message to Play...")
        return
    if (rating_mode_var == 1) :
        status_message.update_message("You can't play during Rating Mode")
        return
    INPUT = INPUT.replace(" ","").upper()
    for i in INPUT:
        cl.play_char(i)


rating_mode_var = tk.IntVar() 
def rating_mode():
    cl.rating_mode = rating_mode_var

def update():
    update_setting()
    update_status()

def update_setting():
    if (rating_mode_var == 1):
        tmp = cl.tone_len[0]
        setting.update(([[tmp],[tmp*3],[tmp*3]]))
    else:
        setting.update(([[cl.tone_len[0]],[cl.tone_len[1]],[cl.tone_len[2]]]))

def update_status():
    stats.update(([st.rating,st.streak,st.session_sum]))


def update_char_type(x):
    cl.char_type = x



# Stat Frame
stat_frame = Subpanel(0,0,"Status:").panel
Infobox(0, 0, 3, 1, [["Rating"],["Streak"],["Session Sum"]], stat_frame)
stats = Infobox(0, 1, 3, 2, [["Current:", "Max:"],["Current:","Max:"],["AC:","WA:"]], stat_frame)

# Setting Frame
setting_frame = Subpanel(0,1,"Settings:",1,3).panel
setting = Infobox(1, 5, 3, 1, [[""],[""],[""]], pos = setting_frame)
m_short = Form(1, cl.tone_len[0], "Set Min Tone", lambda:update_sound_params(m_short,75,200,0), pos = setting_frame)
m_long = Form(2, cl.tone_len[1], "Set Max Tone", lambda:update_sound_params(m_long,225,1000,1), pos = setting_frame)
m_rest = Form(3, cl.tone_len[2], "Set Rest Length", lambda:update_sound_params(m_rest,225,3000,2), pos = setting_frame)

# Option Frame
option_frame = Subpanel(1,1,"Options:",1,3).panel
Message(row = 0, column = 0, message = "Char Type/len:", pos = option_frame)
Message(row = 1, column = 0, message = "Rating Mode:", pos = option_frame)
char_type = Options(0, 1, list = range(1,27), command = lambda x:update_char_type(x), pos = option_frame)
m_char_len = Textbox(0,2,1,5,cl.char_length, pos = option_frame)
Radio_Button(1,1,"On", 1, lambda: rating_mode(), option_frame)
Radio_Button(1,2,"Off", 0, lambda: rating_mode(), option_frame)

# Message Frame
message_frame = Subpanel(3,0,"Messages:",1,4).panel
character_message = Message(row = 7, column = 0, message = "Last Sounds:", colspan=6, pos = message_frame)
status_message = Message(row = 8, column= 0, message = "Status:", colspan=6, pos = message_frame)
error_message = Message(row = 9, column= 0, message = "Error Message:", colspan=6, pos = message_frame)

# Guess Frame
guess_frame = Subpanel(1,0,"Guess:").panel
m_guess = Textbox(0,0,1,35,"",3,guess_frame)
Button(1,0,"Guess",lambda:guess_sound(),guess_frame)
Button(1,1,"Play Game",lambda:guess_game(),guess_frame)
Button(1,2,"Test Sound",lambda:play_sound(),guess_frame)

def run_frame():
    st.init()
    update()
    root.mainloop()
