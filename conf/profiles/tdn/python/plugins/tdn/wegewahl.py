from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QPushButton, QLabel, QDockWidget, QProgressBar, QAction, QMessageBox,  QDialog, QVBoxLayout,QCheckBox,QDialogButtonBox,QScrollArea

vlayer = QgsProject.instance().mapLayersByName("egv_wege")[0]
# Wegeliste erstellen"
wegeliste = []
for feat in vlayer.getFeatures():
    wegeliste.append(feat['Name'])
wegeliste.sort()
        


def checkbox_dialog(items,title="Wege wählen"):
    """
    Erzeugt einen scrollbaren Checkbox-Dialog aus einer Liste.

    :param items: Liste von Strings
    :param title: Fenstertitel
    :param parent: Parent-Widget (z.B. iface.mainWindow())
    :param prechecked: optionale Liste vorausgewählter Einträge
    :return: Liste ausgewählter Einträge oder None bei Abbruch
    """

    #dialog = QDialog(parent)
    dialog = QDialog()
    dialog.setWindowTitle(title)
    dialog.resize(350, 400)

    main_layout = QVBoxLayout(dialog)

    # ScrollArea
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)

    scroll_widget = QWidget()
    scroll_layout = QVBoxLayout(scroll_widget)

    checkboxes = []

    for item in items:
        cb = QCheckBox(str(item))
        scroll_layout.addWidget(cb)
        checkboxes.append(cb)

    scroll_layout.addStretch()
    scroll_area.setWidget(scroll_widget)

    main_layout.addWidget(scroll_area)

    # OK / Cancel Buttons
    button_box = QDialogButtonBox(
        QDialogButtonBox.Ok | QDialogButtonBox.Cancel
    )
    main_layout.addWidget(button_box)

    button_box.accepted.connect(dialog.accept)
    button_box.rejected.connect(dialog.reject)

    if dialog.exec_() == QDialog.Accepted:
        return [
            cb.text()
            for cb in checkboxes
            if cb.isChecked()
        ]
    else:
        return None

wegenamen = checkbox_dialog(wegeliste,"Wege wählen")
print(wegenamen)
