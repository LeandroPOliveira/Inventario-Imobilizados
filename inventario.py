from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.image import Image

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.swiper import MDSwiperItem
import pandas as pd
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.floatlayout import MDFloatLayout
import speech_recognition as sr
import pyttsx3
from functools import partial


class ContentNavigationDrawer(Screen):
    pass


class Principal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label_descr = None
        self.icone = None
        self.num_invent = None
        self.num_serie = None
        self.label_imob = None
        self.inserir_layout = None
        self.insere_denom = None
        self.num_imob = None
        self.insere_swiper = None
        self.listener = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.lista = []
        self.lista_icon = []
        Clock.schedule_once(self.inserir)

    def inserir(self, dt):
        # Buscar dados para alimentar o aplicativo
        dados = pd.read_excel('base.xlsx')
        dados = dados.fillna('')

        for index, row in dados[:4].iterrows():  # Organizar os dados na tela do app
            self.insere_swiper = MDSwiperItem()  # Criar um "swiper" para cada imobilizado
            self.ids.swiper.add_widget(self.insere_swiper)

            self.inserir_layout = MDFloatLayout()  # Adicionar layout para organizar os widgets
            self.insere_swiper.add_widget(self.inserir_layout)

            # inserir os rótulos para cada item
            self.label_imob = MDLabel(pos_hint={'x': 0, 'y': .72}, font_size=20, text='Nº Imobilizado',
                                      size_hint=(1, .2), halign='center')
            self.inserir_layout.add_widget(self.label_imob)
            self.label_descr = MDLabel(pos_hint={'x': 0, 'y': .55}, font_size=20, text='Descrição',
                                       size_hint=(1, .2), halign='center')
            self.inserir_layout.add_widget(self.label_descr)

            # Inserir dados do cadastro
            self.num_imob = MDTextField(text=row['Imobilizado'], pos_hint={'x': 0.15, 'y': .72},
                                    size_hint=(.7, .02), halign='center')
            self.inserir_layout.add_widget(self.num_imob)

            self.insere_denom = MDTextField(text=row['Denominação'], pos_hint={'x': 0.15, 'y': .55},
                                        size_hint=(.7, .1), halign='center')
            self.inserir_layout.add_widget(self.insere_denom)

            self.num_invent = MDTextField(text=row['Nº Inventário'], pos_hint={'x': 0.2, 'y': .4},
                                          size_hint=(.5, .1), hint_text='Nº Inventário', mode="rectangle")
            self.inserir_layout.add_widget(self.num_invent)
            self.lista.append(self.num_invent)
            self.num_serie = MDTextField(text=row['Nº Série'], pos_hint={'x': 0.2, 'y': .25},
                                         size_hint=(.5, .1), hint_text="Nº Série", mode="rectangle")
            self.inserir_layout.add_widget(self.num_serie)

            self.icone = MDIconButton(icon='microphone', icon_size='33sp', pos_hint={'x': 0.71, 'y': .39})
            self.lista_icon.append(self.icone)
            self.inserir_layout.add_widget(self.lista_icon[index])
            self.lista_icon[index].bind(on_press=partial(self.ouvir_numero, index))

        self.ids.swiper.set_current(1)

    def ouvir_numero(self, index, instance):
        try:
            with sr.Microphone() as source:
                print('ouvindo...')
                voz = self.listener.listen(source)
                numero_inventario = self.listener.recognize_google(voz, language='pt-BR')
                if len(numero_inventario) < 6:
                    numero_inventario = str(numero_inventario).zfill(6)
                self.lista[index].text = numero_inventario
        except:
            print('não entendi')

    def gravar(self):
        pass


class Tela2(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class Inventario(MDApp):

    def build(self):
        return Builder.load_file('inventario.kv')


Inventario().run()
