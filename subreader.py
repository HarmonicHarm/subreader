from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp

time = []
text = []
time2 = []

with open('insert file name here', 'r') as subs:
    subs = list(subs)


for i in range(len(subs)):
    if str(subs[i].strip()).isdigit() == True or subs[i].strip() == "ï»¿1":
        continue
    elif subs[i].strip() == "":
        continue
    elif "-->" in subs[i].strip():
        time.append(subs[i].strip())
    else:
        if "-->" not in subs[i-1].strip():
            text[-1] += " " + subs[i].strip()
        else:
            text.append("")
            text.append(subs[i].strip())
            



for i in range(len(time)): 
    time[i] = list(i.split(":") for i in time[i].split(' --> '))

for i in range(len(time)):
    for i2 in range(len(time[i])):
        time[i][i2][0] = int(time[i][i2][0])
        time[i][i2][1] = int(time[i][i2][1])
        time[i][i2][2] = float(time[i][i2][2].replace(",","."))

for i in range(len(time)):
    for i2 in range(len(time[i])):
        time[i][i2] = time[i][i2][0]*60*60 + time[i][i2][1]*60 + time[i][i2][2]

#print(time)
#print("=========================================================================")

for i in range(len(time)):
    if i == 0:
        time2.append(time[0][0] - 0)
        time2.append(time[0][1] - time[0][0])
    else:
        time2.append(time[i][0] - time[i-1][1])
        time2.append(time[i][1] - time[i][0])


"""print(len(time))
print(len(time2))
print(len(text))"""

"""for i in range(50):
    print(i)
    print(text[i])
    print(time2[i])
    print("===================")"""

"""
for i in range(len(time)):
    time[i] = time[i][1] - time[i][0]
"""
"""
sub = dict(zip(time, text))
print(sub)
"""

class HelloWorldApp(App):
    def build(self):
        Window.size = (500,130)
        fs = dp(15)
        #self.label = Label(text="Hello, World!", font_size=30)
        self.layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))  # Use BoxLayout to hold multiple labels

        self.prev_label = Label(text="", font_size=fs, size_hint_y=1, text_size=(None, None), halign='center')
        self.current_label = Label(text="Waiting for text", font_size=fs * 1.5, size_hint_y=1, text_size=(None, None), halign='center') 
        self.next_label = Label(text="", font_size=fs, size_hint_y=1, text_size=(None, None), halign='center')

        self.layout.add_widget(self.prev_label)
        self.layout.add_widget(self.current_label)
        self.layout.add_widget(self.next_label)

        self.buttons_layout = BoxLayout(orientation='horizontal', size_hint=(None,None), height=50, spacing=10)
        self.buttons_layout.pos_hint = {'center_x': 0.5}
        self.prev_button = Button(text="<", on_press=self.prev_text, size_hint=(None, None), size=(50, 50))
        self.next_button = Button(text=">", on_press=self.next_text, size_hint=(None, None), size=(50, 50))


        self.buttons_layout.add_widget(self.prev_button)
        self.buttons_layout.add_widget(self.next_button)

        self.layout.add_widget(self.buttons_layout)

        self.texts = text
        self.intervals = time2
        self.index = 0
        Clock.schedule_once(self.update_text, 0)
        return self.layout
    
    def update_text(self, dt):
        if self.index < len(self.texts):
            if self.texts[self.index].strip() == "":
                self.prev_label.text = self.texts[self.index - 1] if self.index > 0 else ""
                self.current_label.text = self.texts[self.index]
                self.next_label.text = self.texts[self.index + 1] if self.index < len(self.texts) - 1 else ""
            else:
                self.prev_label.text = self.texts[self.index - 2] if self.index > 1 else ""
                self.current_label.text = self.texts[self.index]
                self.next_label.text = self.texts[self.index + 2] if self.index < len(self.texts) - 2 else ""

            interval = self.intervals[self.index]
            self.index += 1
            if self.index < len(self.texts):
                Clock.schedule_once(self.update_text, interval)
        else:
            return False
        
    def prev_text(self, instance):
        if self.index < len(self.texts) - 1:
            Clock.unschedule(self.update_text)
            self.index -= 3
            self.update_text(0)

    def next_text(self, instance):
        # Move index forward and update the tex
        if self.index < len(self.texts) - 1:
            Clock.unschedule(self.update_text)
            self.index += 1
            self.update_text(0)
if __name__ == "__main__":
    HelloWorldApp().run()