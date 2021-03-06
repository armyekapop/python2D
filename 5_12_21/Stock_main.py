from os import getlogin
import kivy
import math
import weakref
import pickle
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
from Stock import *

categories = ['เนื้อสัตว์','ผัก','อาหารทานเล่น','เครื่องดื่ม','ผลไม้','น้ำซุป','ของหวาน', 'น้ำจิ้ม','อื่นๆ']


Config.set('graphics', 'width', '1440')
Config.set('graphics', 'height', '1024')
# Config.set('graphics', 'resizable', False)

isCreatedStock = False
isStock_pickle = open('D:/python/5_12_21/isStock.pkl', 'wb')
pickle.dump(isCreatedStock, isStock_pickle)
isStock_pickle.close()

isStock_pickle = open('D:/python/5_12_21/stock.pkl', 'rb')
isCreatedStock = pickle.load(isStock_pickle)
isStock_pickle.close()

# s = loadStock()

if isCreatedStock:  
    s = loadStock()
else:
    s = Stock('Stock')
    for category in categories:
        s.addCategory(category)
        print(s.getDisplayItem(),55)

ref_dict={}
cat_dict = {}

# Temporary stock
# with open('D:/python/5_12_21/meat.txt') as reader:
#     s.addCategory('Meat1')
#     for line in reader.readlines():
#         a, b = line.split()
#         b=int(b)
#         s.getCategory('Meat1').addNewType(a, b ,24)

def get_len(category):
    if s.getCategory(category).getDisplayItem() == None:
        return 0
    return len(s.getCategory(category).getDisplayItem())

class MainWindow(Screen):
    item = ObjectProperty(None)

    def Btn(self):
        print("Search: ",self.item.text)

    def saveExit(self):
        saveStock(s)
        print('save&exit func...')
    pass

class AddWindow(Screen):
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
        cat_dict['stayAt'] = instance.text
        # print(instance.text)
        self.manager.current = 'categories'
        self.manager.current_screen.ids.titleTXT.text = instance.text

        # items = []
        # with open('meat.txt') as reader:
        #     for line in reader.readlines():
        #         items.append(line)
        # for i in range(len(items)):
        #     items[i] = items[i].split()

        # generate widget.
        n = get_len(cat_dict['stayAt'])/1
        self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n) # กำหนดช่วงความสูงของ GridLayout ใน ScrollView
        for i in range(get_len(cat_dict['stayAt'])):
            label = Label(text=s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][0], font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
            amount = Label(text=str(0), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            add = Button(text="+", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            decrease = Button(text="-", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            clear = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="bin.png")
            reset = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="reset.png")
            total = Label(text = str(s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][1]), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            
            # Add widget.
            self.manager.current_screen.ids.GL.add_widget(clear)
            self.manager.current_screen.ids.GL.add_widget(reset)
            self.manager.current_screen.ids.GL.add_widget(label)
            self.manager.current_screen.ids.GL.add_widget(decrease)
            self.manager.current_screen.ids.GL.add_widget(amount)
            self.manager.current_screen.ids.GL.add_widget(add)
            self.manager.current_screen.ids.GL.add_widget(total)

            ref_dict["add "+str(i)]=weakref.ref(add)
            ref_dict["decrease "+str(i)]=weakref.ref(decrease)
            ref_dict["amt "+str(i)]=weakref.ref(amount)
            ref_dict["total "+str(i)]=weakref.ref(total)
            ref_dict["label "+str(i)]=weakref.ref(label)
            ref_dict["clear "+str(i)]=weakref.ref(clear)
            ref_dict["reset "+str(i)]=weakref.ref(reset)

            add.bind(on_press=self.manager.current_screen.adder)
            decrease.bind(on_press=self.manager.current_screen.decrease)
            clear.bind(on_press=self.manager.current_screen.remove)
            reset.bind(on_press=self.manager.current_screen.reset)

class CategoriesWindow(Screen):
    fmaterialsName = ObjectProperty(None)
    fmaterialsAmount = ObjectProperty(None)
    fmaterialsExpire = ObjectProperty(None)
    def on_kv_post(self, obj):
        pass

    def adder(self, instance):
        a = self.get_id(instance)

        # update amount on screen.
        amt = int(ref_dict["amt "+a]().text)+1
        ref_dict["amt "+a]().text = str(amt)
        # update total.
        ref_dict["total "+a]().text = str(int(s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][1]) + int(amt))

    def decrease(self, instance):
        a = self.get_id(instance)
        
        # update amount on screen.
        if int(ref_dict["amt "+a]().text)>0:
            amt = int(ref_dict["amt "+a]().text)-1
            ref_dict["amt "+a]().text = str(amt)
        # update total.
        ref_dict["total "+a]().text = str(s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][1] + int(ref_dict["amt "+a]().text))

    def remove(self, instance):
        a = self.get_id(instance)
        # loop remove widget.
        for id in ref_dict:
            if a in id:
                self.ids.GL.remove_widget(ref_dict[id]())

                # Move Index to replace old weakref\
                i = id.split()
                for j in range(int(i[-1]), get_len(cat_dict['stayAt'])-1):
                    ref_dict[i[0]+' '+str(j)] = ref_dict[i[0]+' '+str(j+1)]

        print(ref_dict.keys())
        # print(s.printCategory())
        name = s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][0]
        s.getCategory(cat_dict['stayAt']).removeType(name)
        # print(s.getCategory('Meat1').printType())

        n = math.ceil(get_len(cat_dict['stayAt']))
        self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n)

    def reset(self, instance):
        a = self.get_id(instance)

        ref_dict["amt "+a]().text = str(0)
        ref_dict["total "+a]().text = str(s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][1])

    def get_id(self, instance):
        ref_instance = weakref.ref(instance)
        for id in ref_dict:
            if ref_instance == ref_dict[id]:
                return id.split()[-1]

    def back(self):
        print("Button on click: back")
        self.ids.GL.clear_widgets()
        ref_dict.clear()
        self.materialsName.text=""
        self.materialsAmount.text=""
        self.materialsExpire.text=""

    def adding_item(self):
        # print(self.materialsName.text,self.materialsAmount.text,self.materialsExpire.text)
        
        if(self.materialsName.text != '' and self.materialsExpire.text != ''):
            print(self.materialsName.text,self.materialsAmount.text,self.materialsExpire.text)
            if self.materialsAmount.text == '': 
                self.materialsAmount.text = '0'
            s.getCategory(cat_dict['stayAt']).addNewType(self.materialsName.text,int(self.materialsAmount.text) ,int(self.materialsExpire.text))

            label = Label(text=self.materialsName.text, font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
            amount = Label(text=str(0), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            add = Button(text="+", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            decrease = Button(text="-", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            clear = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="bin.png")
            reset = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="reset.png")
            total = Label(text = self.materialsAmount.text, font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)

            self.ids.GL.add_widget(clear)
            self.ids.GL.add_widget(reset)
            self.ids.GL.add_widget(label)
            self.ids.GL.add_widget(decrease)
            self.ids.GL.add_widget(amount)
            self.ids.GL.add_widget(add)
            self.ids.GL.add_widget(total)

            ref_dict["add "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(add)
            ref_dict["decrease "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(decrease)
            ref_dict["amt "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(amount)
            ref_dict["total "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(total)
            ref_dict["label "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(label)
            ref_dict["clear "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(clear)
            ref_dict["reset "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(reset)

            add.bind(on_press=self.adder)
            decrease.bind(on_press=self.decrease)
            clear.bind(on_press=self.remove)
            reset.bind(on_press=self.reset)

            n = math.ceil(get_len(cat_dict['stayAt']))
            self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n)

        self.materialsName.text=""
        self.materialsAmount.text=""
        self.materialsExpire.text=""
        
        # Add amount of Items
        for i in range(get_len(cat_dict['stayAt'])):
            item = ref_dict["label "+str(i)]().text
            amount = ref_dict["amt "+str(i)]().text
            total = ref_dict["total "+str(i)]().text
            print(item, amount, total)
            if int(amount)>0:
                name = s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][0]
                s.getCategory(cat_dict['stayAt']).getType(name).addItem(int(amount))
            ref_dict["amt "+str(i)]().text = str(0)

        print("----------------------------------")
        print(s.getCategory(cat_dict['stayAt']).getDisplayItem())
        
class UseWindow(Screen):
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
        cat_dict['stayAt'] = instance.text
        # print(instance.text)
        self.manager.current = 'usecategories'
        self.manager.current_screen.ids.titleTXT.text = instance.text

        # items = []
        # with open('meat.txt') as reader:
        #     for line in reader.readlines():
        #         items.append(line)
        # for i in range(len(items)):
        #     items[i] = items[i].split()

        # generate widget.
        n = get_len(cat_dict['stayAt'])/1
        self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n) # กำหนดช่วงความสูงของ GridLayout ใน ScrollView
        for i in range(get_len(cat_dict['stayAt'])):
            label = Label(text=s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][0], font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
            amount = Label(text=str(0), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            add = Button(text="+", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            decrease = Button(text="-", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            clear = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="bin.png")
            reset = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="reset.png")
            total = Label(text = str(s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][1]), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            
            # Add widget.
            self.manager.current_screen.ids.GL.add_widget(clear)
            self.manager.current_screen.ids.GL.add_widget(reset)
            self.manager.current_screen.ids.GL.add_widget(label)
            self.manager.current_screen.ids.GL.add_widget(decrease)
            self.manager.current_screen.ids.GL.add_widget(amount)
            self.manager.current_screen.ids.GL.add_widget(add)
            self.manager.current_screen.ids.GL.add_widget(total)

            ref_dict["add "+str(i)]=weakref.ref(add)
            ref_dict["decrease "+str(i)]=weakref.ref(decrease)
            ref_dict["amt "+str(i)]=weakref.ref(amount)
            ref_dict["total "+str(i)]=weakref.ref(total)
            ref_dict["label "+str(i)]=weakref.ref(label)
            ref_dict["clear "+str(i)]=weakref.ref(clear)
            ref_dict["reset "+str(i)]=weakref.ref(reset)

            add.bind(on_press=self.manager.current_screen.adder)
            decrease.bind(on_press=self.manager.current_screen.decrease)
            clear.bind(on_press=self.manager.current_screen.remove)
            reset.bind(on_press=self.manager.current_screen.reset)

class UseCategoriesWindow(Screen):
    fmaterialsName = ObjectProperty(None)
    fmaterialsAmount = ObjectProperty(None)
    fmaterialsExpire = ObjectProperty(None)
    def on_kv_post(self, obj):
        pass

    def adder(self, instance):
        a = self.get_id(instance)

        # update amount on screen.
        amt = int(ref_dict["amt "+a]().text)+1
        ref_dict["amt "+a]().text = str(amt)
        # update total.
        ref_dict["total "+a]().text = str(int(s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][1]) + int(amt))

    def decrease(self, instance):
        a = self.get_id(instance)
        
        # update amount on screen.
        if int(ref_dict["amt "+a]().text)>0:
            amt = int(ref_dict["amt "+a]().text)-1
            ref_dict["amt "+a]().text = str(amt)
        # update total.
        ref_dict["total "+a]().text = str(s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][1] + int(ref_dict["amt "+a]().text))

    def remove(self, instance):
        a = self.get_id(instance)
        # loop remove widget.
        for id in ref_dict:
            if a in id:
                self.ids.GL.remove_widget(ref_dict[id]())

                # Move Index to replace old weakref\
                i = id.split()
                for j in range(int(i[-1]), get_len(cat_dict['stayAt'])-1):
                    ref_dict[i[0]+' '+str(j)] = ref_dict[i[0]+' '+str(j+1)]

        print(ref_dict.keys())
        # print(s.printCategory())
        name = s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][0]
        s.getCategory(cat_dict['stayAt']).removeType(name)
        # print(s.getCategory('Meat1').printType())

        n = math.ceil(get_len(cat_dict['stayAt']))
        self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n)

    def reset(self, instance):
        a = self.get_id(instance)

        ref_dict["amt "+a]().text = str(0)
        ref_dict["total "+a]().text = str(s.getCategory(cat_dict['stayAt']).getDisplayItem()[int(a)][1])

    def get_id(self, instance):
        ref_instance = weakref.ref(instance)
        for id in ref_dict:
            if ref_instance == ref_dict[id]:
                return id.split()[-1]

    def back(self):
        print("Button on click: back")
        self.ids.GL.clear_widgets()
        ref_dict.clear()
        self.materialsName.text=""
        self.materialsAmount.text=""
        self.materialsExpire.text=""

    def adding_item(self):
        # print(self.materialsName.text,self.materialsAmount.text,self.materialsExpire.text)
        
        if(self.materialsName.text != '' and self.materialsExpire.text != ''):
            print(self.materialsName.text,self.materialsAmount.text,self.materialsExpire.text)
            if self.materialsAmount.text == '': 
                self.materialsAmount.text = '0'
            s.getCategory(cat_dict['stayAt']).addNewType(self.materialsName.text,int(self.materialsAmount.text) ,int(self.materialsExpire.text))

            label = Label(text=self.materialsName.text, font_size=24, size_hint_y=None, height=70,font_name='fonts/THSarabun Bold.ttf')
            amount = Label(text=str(0), font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)
            add = Button(text="+", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            decrease = Button(text="-", font_size=48, size_hint_y=None, height=70, size_hint_x=None, width=70)
            clear = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="bin.png")
            reset = Button(size_hint_y=None, height=70, size_hint_x=None, width=70, background_normal="reset.png")
            total = Label(text = self.materialsAmount.text, font_size=24, size_hint_y=None, height=70, size_hint_x=0.1)

            self.ids.GL.add_widget(clear)
            self.ids.GL.add_widget(reset)
            self.ids.GL.add_widget(label)
            self.ids.GL.add_widget(decrease)
            self.ids.GL.add_widget(amount)
            self.ids.GL.add_widget(add)
            self.ids.GL.add_widget(total)

            ref_dict["add "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(add)
            ref_dict["decrease "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(decrease)
            ref_dict["amt "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(amount)
            ref_dict["total "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(total)
            ref_dict["label "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(label)
            ref_dict["clear "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(clear)
            ref_dict["reset "+str(get_len(cat_dict['stayAt'])-1)]=weakref.ref(reset)

            add.bind(on_press=self.adder)
            decrease.bind(on_press=self.decrease)
            clear.bind(on_press=self.remove)
            reset.bind(on_press=self.reset)

            n = math.ceil(get_len(cat_dict['stayAt']))
            self.manager.current_screen.ids.GL.height = (40*(n+1)+70*n)

        self.materialsName.text=""
        self.materialsAmount.text=""
        self.materialsExpire.text=""
        
        # Add amount of Items
        for i in range(get_len(cat_dict['stayAt'])):
            item = ref_dict["label "+str(i)]().text
            amount = ref_dict["amt "+str(i)]().text
            total = ref_dict["total "+str(i)]().text
            print(item, amount, total)
            if int(amount)>0:
                name = s.getCategory(cat_dict['stayAt']).getDisplayItem()[i][0]
                s.getCategory(cat_dict['stayAt']).getType(name).addItem(int(amount))
            ref_dict["amt "+str(i)]().text = str(0)

        print("----------------------------------")
        print(s.getCategory(cat_dict['stayAt']).getDisplayItem())

class WindowManager(ScreenManager):
    pass

KV = Builder.load_file("stock.kv")

class StockApp(App):
    def build(self):
        return KV

if __name__ == "__main__":
    StockApp().run()