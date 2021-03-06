import kivy
import math
import weakref
from kivy.app import App
from kivy.uix.behaviors import button
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import RoundedRectangle,Color
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.utils import interpolate
from stock_back import *
cat_dict = {}
Config.set('graphics', 'width', '1440')
Config.set('graphics', 'height', '1024')
# Config.set('graphics', 'resizable', False)

categories = ['เนื้อสัตว์','ผัก','อาหารทานเล่น','เครื่องดื่ม','ผลไม้','น้ำซุป','ของหวาน', 'น้ำจิ้ม','อื่นๆ', 'New']

stock = loadStock()
stock = Stock('food')
#add categories to stock
for category in categories:
    print(category)
    stock.addCategory(category)
    print(stock.getDisplayItem(),55)
# print(stock.getDisplayItem(),4555555)

ref_dict={}

class Materials:

    def __init__(self):
        self.name = ''
        self.amount = 0
        self.expire = 0.0

    def setName(self, name):
        self.name = name

    def setAmount (self, amount):
        self.amount = amount

    def setExpire(self, expire):
        self.expire = expire

class MainWindow(Screen):
    item = ObjectProperty(None)

    def Btn(self):
        print("Search: ",self.item.text)

    def saveExit(self):
        print('save&exit func...')
    pass

class AddWindow(Screen):
    fmaterialsName = ObjectProperty(None)
    fmaterialsAmount = ObjectProperty(None)
    fmaterialsExpire = ObjectProperty(None)
    def on_kv_post(self, obj):
        n = math.ceil(len(categories)/3)
        self.ids.SV.height = (40*(n-1)+190*(n))
        # loop create categories BTN.
        for i in range(len(categories)):
            button = Button(text=categories[i], font_name='fonts/THSarabun Bold.ttf', font_size = 36, size_hint_y = None, height = 190)
            button.bind(on_press=self.pressed)
            self.ids[categories[i]] = weakref.ref(button)
            # with self.ids[categories[i]].canvas.before:
            #     Color(rgba=(0,0,0,0.3))
            #     RoundedRectangle(size=(1310/3, 190),pos=button.pos, radius = [(40, 40), (40, 40), (40, 40), (40, 40)])
            self.ids.BL1.add_widget(button)

    def pressed(self, instance):
        print("Button on click:", instance.text)
        cat_dict['stay'] = instance.text
        self.manager.current = 'categories'
        self.manager.current_screen.ids.titleTXT.text = instance.text

        # generate widget.
        items = []
        with open('D:\python\Project_Stock-main\meat.txt') as reader:
            for line in reader.readlines():
                items.append(line)
        for i in range(len(items)):
            items[i] = items[i].split()
        n = math.ceil(len(items)/1)
        self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n) # กำหนดช่วงความสูงของ GridLayout ใน ScrollView
        for i in range(len(items)):
            label = Label(text=items[i][0], font_size=24, size_hint_y=None, height=70)
            amount = Label(text=str(0), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            add = Button(text="+", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            decrease = Button(text="-", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            clear = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="bin.png")
            reset = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="reset.png")
            total = Label(text = items[i][1], font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)

            
            # Add widget.
            self.manager.current_screen.ids.GL.add_widget(clear)
            self.manager.current_screen.ids.GL.add_widget(reset)
            self.manager.current_screen.ids.GL.add_widget(label)
            self.manager.current_screen.ids.GL.add_widget(decrease)
            self.manager.current_screen.ids.GL.add_widget(amount)
            self.manager.current_screen.ids.GL.add_widget(add)
            self.manager.current_screen.ids.GL.add_widget(total)

            ref_dict["add"+str(i+1)]=weakref.ref(add)
            ref_dict["decrease"+str(i+1)]=weakref.ref(decrease)
            ref_dict["amt"+str(i+1)]=weakref.ref(amount)
            ref_dict["total"+str(i+1)]=weakref.ref(total)
            ref_dict["label"+str(i+1)]=weakref.ref(label)
            ref_dict["clear"+str(i+1)]=weakref.ref(clear)
            ref_dict["reset"+str(i+1)]=weakref.ref(reset)

            add.bind(on_press=self.manager.current_screen.adder)
            decrease.bind(on_press=self.manager.current_screen.decrease)
            clear.bind(on_press=self.manager.current_screen.remove)
            reset.bind(on_press=self.manager.current_screen.reset)

class CategoriesWindow(Screen):
    def on_kv_post(self, obj):
        pass

    def adder(self, instance):
        a = self.get_id(instance)

        # update amount on screen.
        amt = int(ref_dict["amt"+a]().text)+1
        ref_dict["amt"+a]().text = str(amt)

    def decrease(self, instance):
        a = self.get_id(instance)
        
        # update amount on screen.
        if int(ref_dict["amt"+a]().text)>0:
            amt = int(ref_dict["amt"+a]().text)-1
            ref_dict["amt"+a]().text = str(amt)

    def remove(self, instance):
        a = self.get_id(instance)
        # loop remove widget.
        for id in ref_dict:
            if a in id:
                self.ids.GL.remove_widget(ref_dict[id]())

    def reset(self, instance):
        print("Reset...")

    def get_id(self, instance):
        ref_instance = weakref.ref(instance)
        for id in ref_dict:
            if ref_instance == ref_dict[id]:
                return id[-1]

    def back(self):
        print("Button on click: back")
        self.ids.GL.clear_widgets()
        ref_dict.clear()

    def adding_item(self):
        if(self.materialsName.text != ''):
            print(self.materialsName.text,self.materialsAmount.text,self.materialsExpire.text)
            stock.getCategory(cat_dict['stay']).addNewType(self.materialsName.text,int(self.materialsAmount.text) ,int(self.materialsExpire.text))
            # print(cat_dict['stay'],4312)
        print(stock.printCategory())
class WindowManager(ScreenManager):
    pass

KV = Builder.load_file("stock.kv")

class StockApp(App):
    def build(self):
        return KV

if __name__ == "__main__":
    StockApp().run()