# -*- coding: utf-8 -*-
#
# TODO: добавить документацию.
#

import os

from kivy.uix.image import Image, AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (
    ObjectProperty, DictProperty, StringProperty, BooleanProperty, ListProperty
)

from kivymd.selectioncontrols import MDCheckbox
from kivymd.ripplebehavior import CircularRippleBehavior
from kivymd.button import MDIconButton
from kivymd.list import (
    ILeftBody, ILeftBodyTouch, IRightBodyTouch, TwoLineAvatarIconListItem,
    OneLineListItem, OneLineIconListItem, ThreeLineAvatarIconListItem,
    OneLineAvatarIconListItem
)


class LeftMDIcon(ILeftBodyTouch, MDIconButton):
    pass


class LeftIcon(ILeftBody, Image):
    pass


class RightMDIcon(IRightBodyTouch,  MDIconButton):
    pass


class LeftIconAsync(ILeftBody, AsyncImage):
    pass


class Icon(CircularRippleBehavior, ButtonBehavior, Image):
    pass


class RightButton(IRightBodyTouch,  Icon):
    pass


class CheckWidget(IRightBodyTouch, MDCheckbox):
    pass


class OneSelectCheckWidget(ILeftBodyTouch, MDCheckbox):
    pass


class OneSelectCheckItem(OneLineAvatarIconListItem):
    id = StringProperty()
    group = StringProperty()
    active = BooleanProperty()
    events_callback = ObjectProperty()


class CheckItem(TwoLineAvatarIconListItem):
    events_callback = ObjectProperty()
    '''Функция обработки сигналов экрана.'''

    active = BooleanProperty(False)
    '''Активный ли чекбокс списка или нет.'''

    icon = StringProperty()
    '''Путь к иконке списка.'''


class IconItemThree(ThreeLineAvatarIconListItem):
    events_callback = ObjectProperty()
    icon = StringProperty()


class IconItem(TwoLineAvatarIconListItem):
    events_callback = ObjectProperty()
    icon = StringProperty()


class IconItemOne(OneLineIconListItem):
    events_callback = ObjectProperty()
    icon = StringProperty()


class IconItemAsync(TwoLineAvatarIconListItem):
    events_callback = ObjectProperty()
    icon = StringProperty()


class Item(OneLineListItem):
    events_callback = ObjectProperty()


class SingleIconItem(OneLineIconListItem):
    events_callback = ObjectProperty()
    icon = StringProperty('alert-circle')


class Lists(BoxLayout):
    events_callback = ObjectProperty()
    '''Функция обработки сигналов экрана.'''

    dict_items = DictProperty()
    '''{'Name item': ['Desc item', 'icon_item.png', True/False}.'''

    list_items = ListProperty()
    '''['Desc item', 'icon_item.png', True/False]...'''

    right_icons = ListProperty()
    '''Список путей к иконкам для кнопок,
    использующихся в пункте списка справа.'''

    flag = StringProperty('single_list')

    def __init__(self, **kvargs):
        super(Lists, self).__init__(**kvargs)

        if self.flag == 'two_list_icon_check':
            for name_item in self.dict_items.keys():
                desc_item, icon_item, state_item = \
                    self.dict_items[name_item]
                self.ids.list_items.add_widget(
                    CheckItem(
                        text=name_item, secondary_text=desc_item,
                        icon=icon_item, active=state_item,
                        events_callback=self.events_callback, id=name_item
                    )
                )
        elif self.flag == 'two_list_custom_icon':
            self.two_list_custom_icon(self.dict_items, IconItem)
        elif self.flag == 'two_list_custom_icon_async':
            self.two_list_custom_icon(self.dict_items, IconItemAsync)
        elif self.flag == 'three_list_custom_icon':
            self.three_list_custom_icon(self.dict_items)
        elif self.flag == 'single_list' or self.flag == 'single_list_icon':
            self.single_list(self.list_items)
        elif self.flag == 'one_select_check':
            self.one_select_check()

    def one_select_check(self):
        for text_item in self.dict_items.keys():
            self.ids.list_items.add_widget(
                OneSelectCheckItem(
                    text=text_item, id=text_item,
                    events_callback=self.events_callback,
                    group=self.dict_items[text_item][0],
                    active=self.dict_items[text_item][1]
                )
            )

    def single_list(self, list_items):
        '''
        :param list_items: ['Item one', 'Item two', ...];
                           [['Item one', 'name icon', True/False], ...];

        '''

        if self.flag == 'single_list':
            for name_item in list_items:
                self.ids.list_items.add_widget(
                    Item(
                        text=name_item, events_callback=self.events_callback
                    )
                )
        elif self.flag == 'single_list_icon':
            for name_item in list_items:
                self.ids.list_items.add_widget(
                    SingleIconItem(
                        icon=name_item[1], text=name_item[0],
                        events_callback=self.events_callback
                    )
                )

    def three_list_custom_icon(self, dict_items):
        '''
        :param dict_items: {'Name item': ['Desc item', 'icon_item.png'], ...};

        '''

        list_items = self.ids.list_items

        for name_item in dict_items.keys():
            desc_item, icon_item = dict_items[name_item]
            if desc_item == '':
                name_item += '\n'

            icon_item = IconItemThree(
                text=name_item, secondary_text=desc_item, id=name_item,
                icon=icon_item, events_callback=self.events_callback
            )

            for image in self.right_icons:
                icon_item.add_widget(
                    RightButton(
                        id='{}, {}'.format(
                            name_item, os.path.split(image)[1].split('.')[0]),
                        source=image, on_release=self.events_callback
                    )
                )
            list_items.add_widget(icon_item)

    def two_list_custom_icon(self, dict_items, instance_icon):
       for name_item in dict_items.keys():
            desc_item, icon_item = dict_items[name_item]
            icon_item = instance_icon(
                text=name_item, secondary_text=desc_item, id=name_item,
                icon=icon_item, events_callback=self.events_callback
            )

            for image in self.right_icons:
                right_button = RightButton(source=image)
                icon_item.add_widget(right_button)
            self.ids.list_items.add_widget(icon_item)

