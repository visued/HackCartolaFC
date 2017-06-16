import os
import sys

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
        self.url = 'https://api.cartolafc.globo.com/mercado/status'
        self.r = requests.get(self.url)
        self.status = self.r.json()


        if self.status['status_mercado'] == 1:
            self.status_mer = 'Aberto'
        else:
            self.status_mer = 'Fechado'


        self.status_= 'Mercado: '+ self.status_mer + ' Fecha em: ' + \
                                   str(self.status['fechamento']['dia']) + '/' +\
                                   str(self.status['fechamento']['mes']) + '/' +\
                                   str(self.status['fechamento']['ano']) + ' ' +\
                                   str(self.status['fechamento']['hora']) + ':' +\
                                   str(self.status['fechamento']['minuto'])
        return self.status_


    def build(self):
        self.rv = self.root.ids.rv
        self.popula_listview()


    def popula_listview(self, *args):
        self.url = 'https://api.cartolafc.globo.com/atletas/mercado'
        self.r = requests.get(self.url)
        self.dados = self.r.json()
        self.atletas = self.dados['atletas']
        atletas = []

        for self.detalhe in self.atletas:
            if self.detalhe['foto'] is not None:
                self.foto = self.detalhe['foto'][:-11]+'140x140.png'
            else:
                self.foto = ''
            atletas.append({
                'viewclass': 'Atletas',
                'nome': '[b]'+self.detalhe['nome']+'[/b]' + '\n'+'[color=22FF59]C$'+str(self.detalhe['preco_num'])+'[/color]',
                'link_on_avatar': self.foto,
                'height': dp(100)
            })
        self.rv.data = atletas

if __name__ == '__main__':
    HackFCApp().run()