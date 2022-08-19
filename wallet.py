

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivy.lang import Builder
from datetime import date, datetime
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.label import MDLabel
from pandas import read_csv
from math import fsum
from numpy import where
from ssl import create_default_context
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import email.mime.application


def create_support_file(filename: str):
    try:
        txt = open(f"{filename}", "xt")
        txt.close()
        if "csv" in filename:
            with open(f"{filename}", "w") as f:
                f.write("Importo,Data,Descrizione")
    except FileExistsError:
        pass


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class LoadingPopup(Popup):

    def __init__(self, **kwargs):
        super(LoadingPopup, self).__init__(**kwargs)
        self.background_color = "#0475a6"
        self.background = "#0475a6"
        self.title_color = "black"
        self.title = "Attenzione"
        self.size_hint = (None, None)
        self.size = (700, 700)
        self.content = ContentPopup()


class ContentPopup(MDLabel):

    def __init__(self, **kwargs):
        super(ContentPopup, self).__init__(**kwargs)
        self.text = "Inserire un valore numerico"
        self.font_size = 55
        self.color = "white"
        self.padding_x = 25
        self.line_height = 1.5


class ListaMovimentiRDC(MDCardSwipe):
    text = StringProperty()
    sec_text = StringProperty()
    third_text = StringProperty()
    _python_access = ObjectProperty(None)


class ListaMovimentiBNM(MDCardSwipe):
    text = StringProperty()
    sec_text = StringProperty()
    third_text = StringProperty()
    _python_access = ObjectProperty(None)


KV = '''
<ListaMovimentiRDC>:
    _python_access: movements
    size_hint_y: None
    height: movements.height
    swipe_distance: 1200
    MDCardSwipeLayerBox:
        padding: "8dp"
        MDIconButton:
            id: cestino
            icon: "trash-can"
            on_release:
                app.remove_item_star(root)
    MDCardSwipeFrontBox:
        ThreeLineListItem:
            id: movements
            _no_ripple_effect: True
            text: root.text
            secondary_text: root.sec_text
            tertiary_text: root.third_text
            
<ListaMovimentiBNM>:
    _python_access: movements_bnm
    size_hint_y: None
    height: movements_bnm.height
    swipe_distance: 1200
    MDCardSwipeLayerBox:
        padding: "8dp"
        MDIconButton:
            id: cestino_bnm
            icon: "trash-can"
            on_release:
                app.remove_item_bnm_star(root)
    MDCardSwipeFrontBox:
        ThreeLineListItem:
            id: movements_bnm
            _no_ripple_effect: True
            text: root.text
            secondary_text: root.sec_text
            tertiary_text: root.third_text
            
            
<ContentNavigationDrawer>:
    BoxLayout:
        orientation: "vertical"
        padding: "8dp"
        spacing: "8dp"
        AnchorLayout:
            anchor_x: "left"
            size_hint_y: None
            height: avatar.height
            #Image:
                #id: avatar
                #size_hint: None, None
                #size: "56dp", "56dp"
                #source: "wallet.png"
        MDLabel:
            text: "G-Wall-Et"
            font_style: "Button"
            size_hint_y: None
            height: self.texture_size[1]
        MDLabel:
            text: "Created by Gabro"
            font_style: "Caption"
            size_hint_y: None
            height: self.texture_size[1]

        ScrollView:
            MDList:
                OneLineListItem:
                    text: "Debit card"
                    font_style: "Button"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "rdc_window"
                OneLineListItem:
                    text: "Bank"
                    font_style: "Button"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "bnm_window"
                OneLineListItem:
                    text: "BackUp"
                    font_style: "Button"
                    on_press:
                        app.send_mail()

Screen:
    MDNavigationLayout:
        x: toolbar_main.height

        ScreenManager:
            id: screen_manager

            Screen:
                name: "rdc_window"
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        id: toolbar_main
                        pos_hint: {"top": 1}
                        elevation: 10
                        title: "Menu"
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
    
                    MDBottomNavigation:
                        panel_color: 1, 1, 1, 1
                        MDBottomNavigationItem:
                            name: 'Saldo'
                            id: saldo_window
                            text: 'Saldo'
                            icon: 'bank-check'
                            
                            GridLayout:
                                rows: 4
                                adaptive_width: True
                                canvas.before:
                                    Color:
                                        rgba: 1, 1, 1, 1
                                    Rectangle:
                                        size: self.size
                                        pos: self.pos
                                MDToolbar:
                                    title: "Azzeramento"
                                    MDIconButton:
                                        icon: "trash-can"
                                        md_bg_color: app.theme_cls.primary_color
                                        pos_hint: {"center_x": .5, "center_y": .5}
                                        on_release:
                                            app.clear_csv()
                                BoxLayout:
                                MDLabel:
                                    id: saldo
                                    text: "500"
                                    font_size: 150
                                    halign: "center"
                                    bold: True
                                    size_hint_y: None
                                    height: self.texture_size[1]
                                    text_size: self.width, None    
                                BoxLayout:
    
        
                        MDBottomNavigationItem:
                            name: 'Aggiunta'
                            id: aggiunta_window
                            text: 'Aggiunta'
                            icon: 'bank-transfer-out'
                            GridLayout:
                                rows: 3
                                spacing: 5
                                adaptive_height: True
                                canvas.before:
                                    Color:
                                        rgba: 1, 1, 1, 1
                                    Rectangle:
                                        size: self.size
                                        pos: self.pos
                                BoxLayout:
                                AnchorLayout:
                                    size_hint_y: None
                                    height: 170
                                    orientation: "vertical"
                                    anchor_x: 'center'
                                    anchor_y: 'top'
                                    pad_x: 15
                                    pad_y: 5
                                    canvas.before:
                                        Color:
                                            rgba: 0, 0.4, 0, .7
                                    MDTextField:
                                        id: money_out
                                        multiline: False
                                        hint_text: "Inserisci l'importo"
                                        mode: "rectangle"
                                        keyboard_suggestions: True
                                        use_bubble: True
                                        use_handles: True
                                        size_hint_y: None
                                        size_hint_x: None
                                        width: 710
    
                                GridLayout:
                                    cols: 1
                                    rows: 1
                                    MDRaisedButton:
                                        id: add_money_out
                                        text: "Aggiungi"
                                        background_normal: ""
                                        background_color: (0, 0.5, 0, 0.5)
                                        background_down: ""
                                        size_hint_x: 1
                                        on_press:
                                            self.background_color = (1, 0, 0, 1)
                                        on_release:
                                            self.background_color = (0.5, 0.5, 0, 0.5)
                                            app.add_money_out() 
    
                        MDBottomNavigationItem:
                            name: 'Movimenti'
                            id: movimenti_window
                            text: 'Movimenti'
                            icon: 'bank-transfer'
                            BoxLayout:
                                orientation: "vertical"
                                spacing: "10dp"
                                MDToolbar:
                                    elevation: 10
                                    title: "Lista Movimenti"
                                    MDIconButton:
                                        icon: "refresh"
                                        md_bg_color: app.theme_cls.primary_color
                                        pos_hint: {"center_x": .5, "center_y": .5}
                                        on_release:
                                            app.filerefresh()
                                ScrollView:
                                    scroll_timeout : 130
                                    MDList:
                                        id: movimenti_list
                                        padding: 0

            Screen:
                name: "bnm_window"
                BoxLayout:
                    orientation: 'vertical'
                    BoxLayout:
                        orientation: 'vertical'
                        MDToolbar:
                            id: toolbar_bnm
                            pos_hint: {"top": 1}
                            elevation: 10
                            title: "Menu"
                            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                            
                        MDBottomNavigation:
                            panel_color: 1, 1, 1, 1
                            MDBottomNavigationItem:
                                name: 'Saldo'
                                id: saldo_bnm_window
                                text: 'Saldo'
                                icon: 'bank-check'
                                BoxLayout:
                                    orientation: 'vertical'
                                    canvas.before:
                                        Color:
                                            rgba: 1, 1, 1, 1
                                        Rectangle:
                                            size: self.size
                                            pos: self.pos
                                    GridLayout:
                                        rows: 4
                                        adaptive_width: True
                                        canvas.before:
                                            Color:
                                                rgba: 1, 1, 1, 1
                                            Rectangle:
                                                size: self.size
                                                pos: self.pos
                                        BoxLayout:
                                        MDLabel:
                                            id: saldo_bnm
                                            text: ""
                                            font_size: 150
                                            halign: "center"
                                            bold: True
                                            size_hint_y: None
                                            height: self.texture_size[1]
                                            text_size: self.width, None  
                                        BoxLayout:
        
                            MDBottomNavigationItem:
                                name: 'Aggiunta'
                                id: aggiunta_bnm_window
                                text: 'Aggiunta'
                                icon: 'bank-transfer-out'
                                GridLayout:
                                    rows: 3
                                    spacing: 5
                                    adaptive_height: True
                                    canvas.before:
                                        Color:
                                            rgba: 1, 1, 1, 1
                                        Rectangle:
                                            size: self.size
                                            pos: self.pos
                                    BoxLayout:
                                    AnchorLayout:
                                        size_hint_y: None
                                        height: 170
                                        orientation: "vertical"
                                        anchor_x: 'center'
                                        anchor_y: 'top'
                                        pad_x: 15
                                        pad_y: 5
                                        canvas.before:
                                            Color:
                                                rgba: 0, 0.4, 0, .7
                                        MDTextField:
                                            id: money_bnm_out
                                            multiline: False
                                            hint_text: "Inserisci l'importo"
                                            mode: "rectangle"
                                            keyboard_suggestions: True
                                            use_bubble: True
                                            use_handles: True
                                            size_hint_y: None
                                            size_hint_x: None
                                            width: 710
        
                                    GridLayout:
                                        cols: 1
                                        rows: 1
                                        MDRaisedButton:
                                            id: add_money_out_bnm
                                            text: "Aggiungi"
                                            background_normal: ""
                                            background_color: (0, 0.5, 0, 0.5)
                                            background_down: ""
                                            size_hint_x: 1
                                            on_press:
                                                self.background_color = (1, 0, 0, 1)
                                            on_release:
                                                self.background_color = (0.5, 0.5, 0, 0.5)
                                                app.add_money_out_bnm() 
        
                            MDBottomNavigationItem:
                                name: 'Movimenti'
                                id: movimenti_bnm_window
                                text: 'Movimenti'
                                icon: 'bank-transfer'
        
                                BoxLayout:
                                    orientation: "vertical"
                                    spacing: "10dp"
                                    MDToolbar:
                                        elevation: 10
                                        title: "Lista Movimenti"
                                        MDIconButton:
                                            icon: "refresh"
                                            md_bg_color: app.theme_cls.primary_color
                                            pos_hint: {"center_x": .5, "center_y": .5}
                                            on_release:
                                                app.filerefresh_bnm()
                                    ScrollView:
                                        scroll_timeout : 130
                                        MDList:
                                            id: movimenti_bnm_list
                                            padding: 0

        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
'''


class WALLET(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "BlueGray"

    def build(self):
        """Build KV string"""
        return Builder.load_string(KV)

    def on_start(self):

        giorno, mese, anno = self.scandata()
        with open("fronzoli_month.dat", "r") as file:
            previuos_month = file.readline()
        if mese != previuos_month:
            with open("fronzoli_month.dat", "w") as file:
                file.write(mese)
            self.send_mail()
        self.reload()
        self.reload_bnm()

    def add_money_out(self):
        """Insert spent money for RDC"""
        try:
            float(self.root.ids.money_out.text.split("(")[0])
            money_out = read_csv("wallet.csv")
            giorno, mese, anno = self.scandata()
            try:
                money_out.loc[money_out.shape[0]] = [float(self.root.ids.money_out.text.split("(")[0]),
                                                     f"{giorno}/{mese}/{anno}",
                                                     f"{self.root.ids.money_out.text.split('(')[1]}"]
            except IndexError:
                money_out.loc[money_out.shape[0]] = [float(self.root.ids.money_out.text.split("(")[0]),
                                                     f"{giorno}/{mese}/{anno}",
                                                     f"No Description"]
            self.write_saldo(money_out)
            money_out.to_csv("wallet.csv", index=False)
        except ValueError:
            LoadingPopup().open()
        finally:
            self.root.ids.money_out.text = ""
            self.reload()

    def add_money_out_bnm(self):
        """Insert spent money for Bank"""
        try:
            float(self.root.ids.money_bnm_out.text.split("(")[0])
            money_out_bnm = read_csv("wallet_bnm.csv")
            giorno, mese, anno = self.scandata()

            if len(self.root.ids.money_bnm_out.text.split('(')) >= 2 and f"{self.root.ids.money_bnm_out.text.split('(')[1]}" != "":
                money_out_bnm.loc[money_out_bnm.shape[0]] = [float(self.root.ids.money_bnm_out.text.split("(")[0]),
                                                             f"{giorno}/{mese}/{anno}",
                                                             f"{self.root.ids.money_bnm_out.text.split('(')[1]}"]
            else:
                money_out_bnm.loc[money_out_bnm.shape[0]] = [float(self.root.ids.money_bnm_out.text.split("(")[0]),
                                                             f"{giorno}/{mese}/{anno}",
                                                             f"No Description"]
            self.write_saldo_bnm(money_out_bnm)
            money_out_bnm.to_csv("wallet_bnm.csv", index=False)
        except ValueError:
            LoadingPopup().open()
        finally:
            self.root.ids.money_bnm_out.text = ""
            self.reload_bnm()

    def reload(self):
        with open("fronzoli.dat", "r") as file:
            saldo = file.readline()
        if saldo == "":
            saldo = "500.0"
        self.root.ids["saldo"].text = saldo

    def reload_bnm(self):
        with open("fronzoli_bnm.dat", "r") as file:
            saldo_bnm = file.readline()
        if saldo_bnm == "":
            saldo_bnm = "128.39"
        self.root.ids["saldo_bnm"].text = saldo_bnm

    def filerefresh(self):
        """Refresh Card Movements for RDC"""
        for movimenti_list in reversed(self.root.ids.movimenti_list.children):
            self.root.ids.movimenti_list.remove_widget(movimenti_list)
        money_out = read_csv("wallet.csv")
        for money, dat, desc in zip(money_out.Importo, money_out.Data, money_out.Descrizione):
            self.root.ids.movimenti_list.add_widget(
                ListaMovimentiRDC(text=f"{money}", sec_text=f"{dat}", third_text=f"{desc}"))

    def filerefresh_bnm(self):
        """Refresh Card Movements for Bank"""
        for movimenti_list in reversed(self.root.ids.movimenti_bnm_list.children):
            self.root.ids.movimenti_bnm_list.remove_widget(movimenti_list)
        money_out_bnm = read_csv("wallet_bnm.csv")
        giorno, mese, anno = self.scandata()
        for money, dat, desc in zip(money_out_bnm.Importo, money_out_bnm.Data, money_out_bnm.Descrizione):
            if dat.split("/")[1] == mese:
                self.root.ids.movimenti_bnm_list.add_widget(
                    ListaMovimentiBNM(text=f"{money}", sec_text=f"{dat}", third_text=f"{desc}"))

    def remove_item_star(self, instance):
        """Remove a widget from MDCardSwipe"""
        self.root.ids.movimenti_list.remove_widget(instance)
        money_out = read_csv("wallet.csv")
        f_index = where(money_out.Importo == float(instance.text))[0].tolist()
        s_index = where(money_out.Data == instance.sec_text)[0].tolist()
        t_index = where(money_out.Descrizione == instance.third_text)[0].tolist()
        index_found = list(set(f_index).intersection(s_index, t_index))
        money_out.drop(index_found[0], inplace=True)
        self.write_saldo(money_out)
        money_out.to_csv("wallet.csv", index=False)
        self.reload()

    def remove_item_bnm_star(self, instance):
        """Remove a widget from MDCardSwipe"""
        self.root.ids.movimenti_bnm_list.remove_widget(instance)
        money_out_bnm = read_csv("wallet_bnm.csv")
        f_index = where(money_out_bnm.Importo == float(instance.text))[0].tolist()
        s_index = where(money_out_bnm.Data == instance.sec_text)[0].tolist()
        t_index = where(money_out_bnm.Descrizione == instance.third_text)[0].tolist()
        index_found = list(set(f_index).intersection(s_index, t_index))
        money_out_bnm.drop(index_found[0], inplace=True)
        self.write_saldo_bnm(money_out_bnm)
        money_out_bnm.to_csv("wallet_bnm.csv", index=False)
        self.reload_bnm()

    @staticmethod
    def scandata():
        """Get current Date"""

        oggi = date.today()
        mese = oggi.strftime("%B")
        dat = (oggi.strftime("%d"), mese, oggi.strftime("%Y"))

        return dat

    def clear_csv(self):
        """Manually clear csv"""
        with open("wallet.csv", "w") as f:
            f.write("Importo,Data,Descrizione")
        with open("fronzoli.dat", "w") as file:
            file.write("")
        self.reload()

    @staticmethod
    def write_saldo(money_out):
        with open("fronzoli.dat", "w") as file:
            file.write(str(round(fsum([500, -money_out.Importo.sum()]), 2)))

    @staticmethod
    def write_saldo_bnm(money_out_bnm):
        with open("fronzoli_bnm.dat", "w") as file:
            file.write(str(round(fsum([128.39, -money_out_bnm.Importo.sum()]), 2)))

    def send_mail(self):
        """Send backup file via mail"""

        porta = 465
        password = "tbfiragnhrlxrbze"
        smtp_server = "smtp.gmail.com"
        sender_email = "marketduecci@gmail.com"
        receiver_email = "gabriaquila729@gmail.com"

        # html to include in the body section
        giorno, mese, anno = self.scandata()
        time = datetime.now()
        current_time = time.strftime("%H:%M:%S")
        html = f"""BackUp File {giorno}/{mese}/{anno} Ore {current_time}"""

        # Creating message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "BackUp"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # The MIME types for text/html
        HTML_Contents = MIMEText(html, 'html')

        with open(f"wallet_bnm.csv", "rb") as myfile:
            attach = email.mime.application.MIMEApplication(myfile.read(), _subtype="csv")
        attach.add_header('Content-Disposition', 'attachment', filename=f"wallet_bnm.csv")

        # Attachment and HTML to body message.
        msg.attach(attach)
        msg.attach(HTML_Contents)

        message = """Subject: BackUp"""
        context = create_default_context()

        with SMTP_SSL(smtp_server, porta) as server:
            server.login(sender_email, password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())


create_support_file("wallet.csv")
create_support_file("wallet_bnm.csv")
create_support_file("fronzoli.dat")
create_support_file("fronzoli_bnm.dat")
create_support_file("fronzoli_month.dat")

WALLET().run()
