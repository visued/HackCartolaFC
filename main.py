import os, sys
from datetime import datetime

from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.image import AsyncImage as Image
from kivymd.theming import ThemeManager
from lists import Icon


Builder.load_file('%s/lists.kv' % os.path.split(os.path.abspath(sys.argv[0]))[0])


import requests


class HackFCApp(App):
    theme_cls = ThemeManager()

    def get_StatusMercado(self, *args):
        url = 'https://api.cartolafc.globo.com/mercado/status'
        r = requests.get(url)
        status = r.json()

        status_mer = ''
        if status['status_mercado'] == 1:
            status_mer = "Marcado Aberto: Fecha em %s"% datetime.fromtimestamp(
                int(statu_mer['fechamento']['timestamp']).strftime("%Y/%m/%d %H:%m")))
        else:
            status_mer = 'Mercado Fechado'

        return status_mer



    def build(self):
        self.rv = self.root.ids.rv
        self.popula_listview()
        self.menu_items = [
            {'viewclass': 'MDMenuItem', 'text': 'Classificar por:'},
            {'viewclass': 'MDMenuItem', 'text': 'Example item'},
            {'viewclass': 'MDMenuItem', 'text': 'Example item'},
            {'viewclass': 'MDMenuItem', 'text': 'Example item'},
            {'viewclass': 'MDMenuItem', 'text': 'Example item'},
            {'viewclass': 'MDMenuItem', 'text': 'Example item'},
            {'viewclass': 'MDMenuItem', 'text': 'Example item'},
        ]

    def proccess_atleta(self, atleta):
        foto = ''
        try:
            foto = atleta['foto'][:-11]+'140x140.png'
        except :
            pass

        a = {
            'viewclass': 'Atletas',
            'nome': '[b]%s[/b]\n[color=22FF59]C$ %s[/color]'%(
                atleta['apelido'], atleta['preco_num']),
            'link_on_avatar': foto,
            'height': dp(80)
        }
        return a

    def popula_listview(self, *args):
        url = 'https://api.cartolafc.globo.com/atletas/mercado'
        r = requests.get(url)
        dados = r.json()
        atletas = dados['atletas']

        self.rv.data = [self.proccess_atleta(a) for a in atletas]

if __name__ == '__main__':
    HackFCApp().run()
