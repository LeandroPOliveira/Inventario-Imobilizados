import sqlite3
#import pandas as pd
import xlsxwriter
from kivy.config import Config
from kivy.uix.label import Label
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'width', '389')
Config.set('graphics', 'height', '800')
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import datetime
import os
# from android.permissions import request_permissions, Permission
# request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])


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
        self.lista = []
        self.lista_icon = []
        self.lista2 = []

    def inserir(self):
        # Buscar dados para alimentar o aplicativo
        if len(self.lista) != 0:
            for i in self.lista2:
                self.ids.swiper.remove_widget(i)

            self.lista.clear()
        # Organizar os dados na tela do app
        for index, linha in enumerate(self.manager.get_screen('lista').lista):
            self.lista.append([])
            self.insere_swiper = MDSwiperItem()  # Criar um "swiper" para cada imobilizado
            self.lista2.append(self.insere_swiper)
            self.ids.swiper.add_widget(self.insere_swiper)

            self.inserir_layout = MDFloatLayout()  # Adicionar layout para organizar os widgets
            self.insere_swiper.add_widget(self.inserir_layout)

            # inserir os rótulos para cada item
            self.label_imob = MDLabel(pos_hint={'x': 0, 'y': .72}, font_size=20, text='Nº Imobilizado',
                                      size_hint=(1, .2), halign='center')
            self.inserir_layout.add_widget(self.label_imob)
            self.label_descr = MDLabel(pos_hint={'x': 0, 'y': .61}, font_size=20, text='Descrição',
                                       size_hint=(1, .2), halign='center')
            self.inserir_layout.add_widget(self.label_descr)

            # Inserir dados do cadastro
            self.num_imob = Label(text=linha[0], pos_hint={'x': 0.15, 'y': .76}, color=(33/255, 150/255, 243/255, 1),
                                  font_size='25dp', size_hint=(.7, .02), halign='center')
            self.inserir_layout.add_widget(self.num_imob)
            self.lista[index].append(self.num_imob)
            self.insere_denom = MDTextField(text=linha[1][:30], pos_hint={'x': 0.1, 'y': .6},
                                            size_hint=(.8, .1), halign='center', multiline=True)
            self.inserir_layout.add_widget(self.insere_denom)
            self.lista[index].append(self.insere_denom)
            self.num_invent = MDTextField(text=str(linha[2]).zfill(6), pos_hint={'x': 0.25, 'y': .5},
                                          size_hint=(.5, .1), hint_text='Nº Inventário', mode="rectangle")
            self.inserir_layout.add_widget(self.num_invent)
            self.lista[index].append(self.num_invent)
            self.num_serie = MDTextField(text=str(linha[3]), pos_hint={'x': 0.25, 'y': .4},
                                         size_hint=(.5, .1), hint_text="Nº Série", mode="rectangle")
            self.inserir_layout.add_widget(self.num_serie)
            self.lista[index].append(self.num_serie)

            self.lista[index].append(self.num_imob)

        self.insere_swiper2 = MDSwiperItem()
        self.lista2.append(self.insere_swiper2)
        self.ids.swiper.add_widget(self.insere_swiper2)
        self.ids.swiper.set_current(1)

    def gravar(self):
        conn = sqlite3.connect('base')
        cursor = conn.cursor()

        for imob in self.lista:
            cursor.execute('UPDATE inventario set Denominação = ?, Inventario = ?, Serie = ?, '
                           'data_mod = ? where Imobilizado = ?', (imob[1].text, imob[2].text, imob[3].text,
                                                                  datetime.date.today(), imob[0].text))

        conn.commit()
        conn.close()

        self.atual_dialog = MDDialog(text="Registro alterado com sucesso!", radius=[20, 7, 20, 7], )
        self.atual_dialog.open()


class Lista(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dados_listagem = None
        self.lista = []

    def listagem_imobs(self):
        self.dados_listagem = MDDataTable(pos_hint={'center_x': 0.5, 'center_y': 0.525},
                                          size_hint=(.9, 0.7), use_pagination=True,
                                          rows_num=len(self.manager.get_screen('pesquisar').resultado),
                                          background_color_header=get_color_from_hex("#0bbd6d"),
                                          background_color_selected_cell=get_color_from_hex("#d2f7e7"),
                                          check=True, pagination_menu_height='140dp',
                                          column_data=[("[color=#ffffff]Imobilizado[/color]", dp(30)),
                                                       ("[color=#ffffff]Descrição[/color]", dp(40)),
                                                       ("[color=#ffffff]Nº Inventário[/color]", dp(20)),
                                                       ("[color=#ffffff]Nº Serie[/color]", dp(20)),
                                                       ("[color=#ffffff]Data[/color]", dp(20)),
                                                       ("[color=#ffffff]Valor[/color]", dp(20)),
                                                       ],
                                          row_data=self.manager.get_screen('pesquisar').resultado, elevation=1)

        self.add_widget(self.dados_listagem)

    def pegar_check(self):  # Selecionar notas a serem editadas
        self.lista.clear()
        for item in self.dados_listagem.get_row_checks():
            self.lista.append(item)
        self.manager.current = 'principal'


class TelaPesquisa(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.erro_dialog = None
        self.resultado = None

    def buscar(self):
        conn = sqlite3.connect('base')
        cursor = conn.cursor()

        cursor.execute(
            'select Imobilizado, Denominação, Inventario, Serie, Data, Valor from inventario where Denominação like case '
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
            self.manager.current = 'lista'
        conn.close()


class ScriptSap(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.script_dialog = None

    def gerar_script(self):
        conn = sqlite3.connect('base')
        cursor = conn.cursor()

        cursor.execute(
            'select Imobilizado, Denominação, Inventario, Serie from inventario where data_mod >= ? and data_mod <= ?',
            (datetime.datetime.strptime(self.ids.data_mod_ini.text, "%d/%m/%Y").date(),
             datetime.datetime.strptime(self.ids.data_mod_fim.text, "%d/%m/%Y").date()))
        dados_script = cursor.fetchall()

        # app_folder = os.getenv('EXTERNAL_STORAGE') or os.path.expanduser("~")
        app_folder = self.ids.caminho.text
        # Abrir arquivo de script gerado pelo SAP
        arquivo = open(os.path.join(app_folder, 'descricao.vbs'),
                       'w')  # modo 'a' de append, insere novos dados no arquivo sem excluir os que estavam

        arquivo.write(f'''
If Not IsObject(application) Then
   Set SapGuiAuto  = GetObject("SAPGUI")
   Set application = SapGuiAuto.GetScriptingEngine
End If
If Not IsObject(connection) Then
   Set connection = application.Children(0)
End If
If Not IsObject(session) Then
   Set session    = connection.Children(0)
End If
If IsObject(WScript) Then
   WScript.ConnectObject session,     "on"
   WScript.ConnectObject application, "on"
End If
''')

        # iterar sobre as linhas do arquivo excel e buscar os dados necessários para o script
        for linha in dados_script:
            # Adicionar os dados ao script
            arquivo.write(f'''
session.findById("wnd[0]").maximize
session.findById("wnd[0]/tbar[0]/okcd").text = "as02"
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/usr/ctxtANLA-ANLN1").text = "{linha[0].split('-')[0]}"
session.findById("wnd[0]/usr/ctxtANLA-ANLN2").text = "{linha[0].split('-')[1]}"
session.findById("wnd[0]/usr/ctxtANLA-ANLN2").setFocus
session.findById("wnd[0]/usr/ctxtANLA-ANLN2").caretPosition = 1
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/usr/subTABSTRIP:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0200/subAREA1:SAPLAIST:1140/txtANLH-ANLHTXT").text = "{linha[1]}"
session.findById("wnd[0]/usr/subTABSTRIP:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0200/subAREA1:SAPLAIST:1140/txtANLA-SERNR").text = "{linha[3] if linha[3] != 'None' else ''}"
session.findById("wnd[0]/usr/subTABSTRIP:SAPLATAB:0100/tabsTABSTRIP100/tabpTAB01/ssubSUBSC:SAPLATAB:0200/subAREA1:SAPLAIST:1140/txtANLA-INVNR").text = "{linha[2] if linha[2] != 'None' else ''}"
session.findById("wnd[0]/tbar[0]/btn[11]").press
session.findById("wnd[0]/tbar[0]/btn[3]").press
''')

        self.script_dialog = MDDialog(text='Script gerado com sucesso!', radius=[20, 7, 20, 7], )
        self.script_dialog.open()


class Relatorio(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.relat_dialog = None

    def gerar_relatorio(self):
        conn = sqlite3.connect('base')
        cursor = conn.cursor()
        cursor.execute('select * from inventario')
        resultado = cursor.fetchall()
        print(resultado)
        pasta = self.ids.caminho_rel.text
        workbook = xlsxwriter.Workbook((os.path.join(pasta, 'Relatório.xlsx')))
        worksheet = workbook.add_worksheet()
        for index, linha in enumerate(resultado):
            worksheet.write(index, 0, linha[0])
            worksheet.write(index, 1, linha[1])
            worksheet.write(index, 2, linha[2])
            worksheet.write(index, 3, linha[3])
            worksheet.write(index, 4, linha[4])
            worksheet.write(index, 5, linha[5])
            worksheet.write(index, 6, linha[6])
            worksheet.write(index, 7, linha[7])
        workbook.close()
        # query_sql = pd.read_sql_query('select * from inventario', conn)
        # dados_relatorio = pd.DataFrame(query_sql)


        # writer = pd.ExcelWriter((os.path.join(pasta, 'Relatório.xlsx')), engine='xlsxwriter', date_format='DD/MM/YYYY')
        # dados_relatorio.to_excel(writer, sheet_name='Sheet1', index=False)
        # writer.save()
        # pasta = self.ids.caminho_rel.text
        # dados_relatorio.to_excel(os.path.join(pasta, 'Relatório.xlsx'), index=False)

        self.relat_dialog = MDDialog(text='Relatório gerado com sucesso!', radius=[20, 7, 20, 7], )
        self.relat_dialog.open()


class WindowManager(ScreenManager):
    pass


class Inventario(MDApp):
    pass

    def build(self):
        return Builder.load_file('main.kv')


Inventario().run()
