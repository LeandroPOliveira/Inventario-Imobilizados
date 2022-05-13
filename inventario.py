from kivy.config import Config

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.swiper import MDSwiperItem
import pandas as pd

from kivymd.uix.button import MDRectangleFlatButton

class ContentNavigationDrawer(Screen):
    pass


class Principal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.insere_denom = None
        self.insere_imob = None
        self.insere_swiper = None

    def inserir(self):
        dados = pd.read_excel('base.xlsx')
        for index, row in dados.iterrows():
            self.insere_swiper = MDSwiperItem()
            # self.insere_swip.id = f'teste{index}'
            self.ids.swip.add_widget(self.insere_swiper)
            self.insere_imob = MDRectangleFlatButton(text=row['Imobilizado'], pos_hint={'x': 0, 'y': .7},
                                       size_hint=(1, .2), halign='center')
            self.insere_denom = MDRectangleFlatButton(text=row['Denominação'], pos_hint={'x': 0, 'y': .4},
                                        size_hint=(1, .2), halign='center')
            # lista = [self.insere, self.insere_denom]
            # for i in lista:
            #     self.insere_swip.add_widget(i)
            self.insere_swiper.add_widget(self.insere_imob)
            self.insere_swiper.add_widget(self.insere_denom)


class Tela2(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class Inventario(MDApp):

    def build(self):
        return Builder.load_file('inventario.kv')


Inventario().run()
