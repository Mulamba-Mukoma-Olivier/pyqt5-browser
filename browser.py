from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QUrl, Qt
import requests
import socket
import uuid
from datetime import datetime


# =========================
# Informations de la machine
# =========================

mac = uuid.getnode()

mac_address = ':'.join(
    f'{(mac >> i) & 0xff:02x}'
    for i in range(40, -1, -8)
)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

server_url = 'http://localhost:8001/send'


class Browser(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi("browser.ui", self)

        self.setWindowFlags(Qt.FramelessWindowHint)

        # Boutons
        self.urlbutton.clicked.connect(self.load_url)
        self.refresh.clicked.connect(self.reaload_func)
        self.back.clicked.connect(self.back_screen)
        self.forward.clicked.connect(self.next_screen)
        self.close_button.clicked.connect(self.close)
        self.redius.clicked.connect(self.showMinimized)
        self.full.clicked.connect(self.toggle_maximize)

    # =========================
    # Chargement d'une URL
    # =========================

    def load_url(self):

        text = self.urlbar.text().strip()

        if not text:
            return

        # Ajouter https:// si nécessaire
        if not text.startswith(("http://", "https://")):
            text = "https://" + text

        # Charger la page
        self.webview.load(QUrl(text))

        # Envoyer les informations au serveur
        self.sendToServer(text)

    # =========================
    # Envoi vers FastAPI
    # =========================

    def sendToServer(self, url):

        now = datetime.now().isoformat()

        data = {
            "ip_address": ip_address,
            "mac_address": mac_address,
            "url": url,
            "timestamp": now
        }

        print("Données envoyées :", data)

        try:

            response = requests.post(
                server_url,
                json=data,
                timeout=5
            )

            print("Status :", response.status_code)
            print("Réponse :", response.text)

        except requests.exceptions.RequestException as e:

            print("Erreur lors de l'envoi :", e)

    # =========================
    # Actualiser
    # =========================

    def reaload_func(self):
        self.webview.reload()
        print("reloaded")

    # =========================
    # Retour
    # =========================

    def back_screen(self):
        self.webview.back()
        print("backed")

    # =========================
    # Suivant
    # =========================

    def next_screen(self):
        self.webview.forward()
        print("forward")

    # =========================
    # Maximiser / restaurer
    # =========================

    def toggle_maximize(self):

        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()