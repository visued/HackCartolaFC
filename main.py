from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage as Image
from kivymd.selectioncontrols import MDCheckbox


from kivymd.theming import ThemeManager
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, MDList, TwoLineAvatarListItem
from kivymd.button import MDIconButton


import requests


class Controller(BoxLayout):
    pass

class HackFCApp(App):
    theme_cls = ThemeManager()


    def build(self):
        pass

    def get_StatusMercado(self):
        self.url = 'https://api.cartolafc.globo.com/mercado/status'
        self.r = requests.get(self.url)
        self.status = self.r.json()


        if self.status['status_mercado'] == 1:
            self.status_mer = 'Fechado'
        else:
            self.status_mer = 'Aberto'


        self.status_= 'Mercado: '+ self.status_mer + ' Fecha em: ' + \
                                   str(self.status['fechamento']['dia']) + '/' +\
                                   str(self.status['fechamento']['mes']) + '/' +\
                                   str(self.status['fechamento']['ano']) + ' ' +\
                                   str(self.status['fechamento']['hora']) + ':' +\
                                   str(self.status['fechamento']['minuto'])
        return self.status_


    def popula_listview(self):
        self.url = 'https://api.cartolafc.globo.com/atletas/mercado'
        self.r = requests.get(self.url)
        self.dados = self.r.json()
        self.atletas = self.dados['atletas']

        for self.detalhe in self.atletas:
            self.mdlist = self.root.ids.mdlist
            if self.detalhe['foto'] is not None:
                self.foto = self.detalhe['foto'][:-11]+'140x140.png'
            else:
                self.foto = ''
            item = TwoLineAvatarListItem(text=self.detalhe['nome'], secondary_text=str(self.detalhe['preco_num']))
            avatar = AvatarSampleWidget(source=self.foto)
            item.add_widget(avatar)
            self.mdlist.add_widget(item)


class AvatarSampleWidget(ILeftBody, Image):
    pass


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass


if __name__ == '__main__':
    HackFCApp().run()