from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QImage, QColor
from PyQt5.QtCore import Qt
from PIL import Image
from excelfinal import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and dimensions
        self.setWindowTitle("Optimisation du service de livraison")
        self.setGeometry(100, 100, 1800, 1400)

        # Create a central widget and a layout for it
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        title_label = QLabel("Plateforme d'optimisation du service de livraison Express", self)
        title_label.setStyleSheet("color: #363636")  # Change the font color to #363636
        font = QFont()
        font.setBold(True)
        font.setPointSize(18)
        title_label.setFont(font)
        layout.addWidget(title_label, alignment=Qt.AlignHCenter)

        # Create a button for browsing the Excel file
        browse_button = QPushButton("Sélectionnez un fichier Excel", self)
        browse_button.setFixedSize(300, 50)
        browse_button.clicked.connect(self.browse_file)
        browse_button.setStyleSheet("QPushButton {"
                                    "    background-color: #17174a;"  # Set background color to red
                                    "    color: #FFFFFF;"  # Set text color to white
                                    "    font-weight: bold;"
                                    "    border-radius: 10px;"  # Set text font weight to bold
                                    "}")
        layout.addWidget(browse_button, alignment=Qt.AlignCenter)

        capacity_label = QLabel("Entrez la capacité des livreurs", self)
        font = QFont()
        capacity_label.setStyleSheet("color: #363636")
        font.setBold(True)
        font.setPointSize(15)
        capacity_label.setFont(font)

        self.setCentralWidget(capacity_label)

        layout.addWidget(capacity_label)

        layout.addWidget(capacity_label, alignment=Qt.AlignCenter)
        self.capacity_entry = QLineEdit(self)
        self.capacity_entry.setFixedSize(300, 50)
        self.capacity_entry.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.capacity_entry, alignment=Qt.AlignCenter)

        resolve_button = QPushButton("Résoudre par  GB", self)
        resolve_button.setFixedSize(300, 50)
        resolve_button.setStyleSheet("QPushButton {"
                                     "    background-color: #17174a;"
                                     "    color: #FFFFFF;"
                                     "    font-weight: bold;"
                                     "    border-radius: 10px;"
                                     "}")
        resolve_button.clicked.connect(self.resolve)
        layout.addWidget(resolve_button, alignment=Qt.AlignCenter)

        # Create a button for resolving with ACO
        resolve_button_aco = QPushButton("Résoudre par ACS", self)
        resolve_button_aco.setFixedSize(300, 50)
        resolve_button_aco.setStyleSheet("QPushButton {"
                                         "    background-color: #17174a;"
                                         "    color: #FFFFFF;"
                                         "    font-weight: bold;"
                                         "    border-radius: 10px;"
                                         "}")
        resolve_button_aco.clicked.connect(self.resolve_aco)
        layout.addWidget(resolve_button_aco, alignment=Qt.AlignCenter)

        logo_image = QPixmap("جامعة_العلوم_والتكنولوجيا_هواري_بومدين.png")
        logo_image = logo_image.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label = QLabel(self)
        logo_label.setPixmap(logo_image)
        logo_label.setStyleSheet("background-color: transparent;")
        logo_label.setGeometry(15, 15, 200, 100)

        logo_image1 = QPixmap("image_viber_2022-12-10_11-19-17-782.png")

        logo_image1 = logo_image1.scaled(200, 150, Qt.AspectRatioMode.KeepAspectRatio)

        logo_label1 = QLabel(self)
        logo_label1.setPixmap(logo_image1)
        logo_label1.setGeometry(1700, 15, 200, 100)

        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        logo_image2 = QPixmap(
            "Asset 4@3x.png")

        logo_image2 = logo_image2.scaled(600, 450, Qt.AspectRatioMode.KeepAspectRatio)

        logo_label2 = QLabel(self)
        logo_label2.setPixmap(logo_image2)

        logo_label2.setGeometry(15, 900, 200, 100)

        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.selected_file_path = ""

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier Excel", "", "Excel files (*.xlsx)")
        print("This is the file path:", file_path)
        self.selected_file_path = file_path

    def resolve(self):
        # Get the selected file path and capacity
        file_path = self.selected_file_path
        capacity = int(self.capacity_entry.text())

        clusters, D, k, ad = zones(file_path, capacity)

        solutions = Tournée(clusters, D, ad)

        self.display_results(k, solutions)

    def resolve_aco(self):
        # Get the selected file path and capacity
        file_path = self.selected_file_path
        capacity = int(self.capacity_entry.text())

        clusters, D, k,ad = zones(file_path, capacity)

        solutions = tournee_ACO(clusters, D, ad)

        self.display_results(k, solutions)

    def display_results(self, k, solutions):
        # Clear the layout
        layout = self.centralWidget().layout()
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        # Create a scroll area to hold the results
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.setCentralWidget(scroll_area)

        results_widget = QWidget()
        scroll_area.setWidget(results_widget)

        results_layout = QVBoxLayout(results_widget)
        results_layout.setContentsMargins(20, 20, 20, 20)  #
        results_layout.setSpacing(20)  # Set spacing between solution frames

        # Create a label for the number of delivery people
        result_k = QLabel(f"Le nombre de livreurs nécessaire est : {k}", self)
        result_k.setAlignment(Qt.AlignLeading)
        result_k.setStyleSheet("font-weight: bold; font-size: 20px; color: #FF0000; margin-bottom: 20px;")
        results_layout.addWidget(result_k)

        # Create a box for each solution
        for i, solution in enumerate(solutions):
            solution_frame = QFrame(self)
            solution_frame.setObjectName("SolutionFrame")
            solution_frame.setStyleSheet("#SolutionFrame { background-color: #F0F0F0; border: 1px solid gray; "
                                         "border-radius: 10px; padding: 20px; }")
            solution_layout = QVBoxLayout(solution_frame)

            # Create QLabel for solution title
            result_label = QLabel(f"Tournée de la zone {i + 1}:", self)
            result_label.setAlignment(Qt.AlignLeft)
            result_label.setStyleSheet("font-weight: bold; font-size: 18px; color: #17174a;")
            solution_layout.addWidget(result_label)

            # Create QLabel for solution text
            cost = solution[-1]
            solution.remove(cost)
            result_text = "|   ,    | ".join(map(str, solution))
            result_text_label = QLabel(result_text, self)
            result_text_label.setAlignment(Qt.AlignLeft)
            result_text_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #333333;")
            solution_layout.addWidget(result_text_label)
            # Create QLabel for cost
            cost_text = QLabel(f"Distance parcourue : {cost} Km", self)
            cost_text.setAlignment(Qt.AlignLeft)
            cost_text.setStyleSheet("font-size: 18px; color: #333333;")
            solution_layout.addWidget(cost_text)

            # Add the solution frame to the results layout
            results_layout.addWidget(solution_frame)
        results_layout.addStretch()

        # Update the layout
        layout.addStretch()
        layout.update()


# Create the application instance
app = QApplication([])

# Create the main window
window = MainWindow()

# Show the main window
window.show()

# Start the application event loop
app.exec_()
