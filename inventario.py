import sqlite3
from kivy.config import Config

Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
import speech_recognition as sr
import pyttsx3
from functools import partial
import datetime


class ContentNavigationDrawer(Screen):
    pass


class Principal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.atual_dialog = None
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

    def inserir(self):
        # Buscar dados para alimentar o aplicativo

        # Organizar os dados na tela do app
        for index, linha in enumerate(self.manager.get_screen('pesquisar').resultado):
            self.lista.append([])
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
            self.num_imob = MDTextField(text=linha[0], pos_hint={'x': 0.15, 'y': .72},
                                        size_hint=(.7, .02), halign='center')
            self.inserir_layout.add_widget(self.num_imob)
            self.lista[index].append(self.num_imob)
            self.insere_denom = MDTextField(text=linha[1], pos_hint={'x': 0.15, 'y': .55},
                                            size_hint=(.7, .1), halign='center')
            self.inserir_layout.add_widget(self.insere_denom)
            self.lista[index].append(self.insere_denom)
            self.num_invent = MDTextField(text=str(linha[2]).zfill(6), pos_hint={'x': 0.2, 'y': .4},
                                          size_hint=(.5, .1), hint_text='Nº Inventário', mode="rectangle")
            self.inserir_layout.add_widget(self.num_invent)
            self.lista[index].append(self.num_invent)
            self.num_serie = MDTextField(text=str(linha[3]), pos_hint={'x': 0.2, 'y': .25},
                                         size_hint=(.5, .1), hint_text="Nº Série", mode="rectangle")
            self.inserir_layout.add_widget(self.num_serie)
            self.lista[index].append(self.num_serie)
            self.icone = MDIconButton(icon='microphone', icon_size='33sp', pos_hint={'x': 0.71, 'y': .39})
            self.lista_icon.append(self.icone)
            self.inserir_layout.add_widget(self.lista_icon[index])
            self.lista_icon[index].bind(on_press=partial(self.ouvir_numero, index))
            self.ident = MDLabel(text=str(linha[4]))
            self.lista[index].append(self.ident)

        self.insere_swiper2 = MDSwiperItem()
        self.ids.swiper.add_widget(self.insere_swiper2)
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
        conn = sqlite3.connect('base')
        cursor = conn.cursor()

        for imob in self.lista:
            cursor.execute('UPDATE inventario set Imobilizado = ?, Denominação = ?, Inventario = ?, Serie = ? where '
                           '[index] = ?', (imob[0].text, imob[1].text, imob[2].text, imob[3].text, int(imob[4].text)))

        conn.commit()
        conn.close()
        
        self.atual_dialog = MDDialog(text="Registro alterado com sucesso!", radius=[20, 7, 20, 7], )
        self.atual_dialog.open()

class TelaPesquisa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.erro_dialog = None
        self.resultado = None

    def buscar(self):
        conn = sqlite3.connect('base')
        cursor = conn.cursor()

        cursor.execute(
            'select Imobilizado, Denominação, Inventario, Serie, [index] from inventario where Denominação like case '
            'when ? != "" then ? else "%" end and Classe like '
            'case when ? != "" then ? else "IES-%" END and Data >= case when ? != "" '
            'then ? else "2000-01-01 00:00:00" end and Data <= case when ? != ""'
            'then ? else "2100-01-01 00:00:00" end and Inventario like case when ? != "" then ? else "%" end',
            (self.ids.descricao.text, "%" + self.ids.descricao.text + "%", self.ids.classe.text, self.ids.classe.text,
             datetime.datetime.strptime(self.ids.data_ini.text, "%d/%m/%Y") if self.ids.data_ini.text != ''
             else '', datetime.datetime.strptime(self.ids.data_ini.text, "%d/%m/%Y") if
             self.ids.data_ini.text != '' else '', datetime.datetime.strptime(self.ids.data_fim.text, "%d/%m/%Y") if
             self.ids.data_ini.text != '' else '',
             datetime.datetime.strptime(self.ids.data_fim.text, "%d/%m/%Y") if self.ids.data_ini.text != ''
             else '', self.ids.num_invent.text, self.ids.num_invent.text))

        self.resultado = cursor.fetchall()
        if len(self.resultado) == 0:
            self.erro_dialog = MDDialog(text="A pesquisa não retornou resultados!", radius=[20, 7, 20, 7], )
            self.erro_dialog.open()
        else:
            self.manager.current = 'principal'
        conn.close()


class WindowManager(ScreenManager):
    pass


class Inventario(MDApp):
    pass
    # def build(self):
    #     return Builder.load_file('inventario.kv')


Inventario().run()
