import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QListWidget, QListWidgetItem

import random

from one_screen import Ui_mainWindow # импортирование UI интерфейса
from two_screen import Ui_TrainingWindow
from three_screen import Ui_CreatCardsWindow
from four_screen import Ui_ListCardsWindow
from five_screen import Ui_StatisticsWindow

class MainWindow(QMainWindow, Ui_mainWindow): # основное окно
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.true_answer = 0
        self.false_answer = 0
        self.all_cards = {}

        self.create_cards_window = CreatCardsWindow(self) # создание окон
        self.list_cards_window = ListCardsWindow(self)
        self.training_window = TrainingWindow(self)
        self.statistics_window = StatisticsWindow(self)

        self.creat_cards_button.clicked.connect(self.open_create_cards_screen) # связка нажатой кнопки с соответствующим окном
        self.training_button.clicked.connect(self.open_training_screen)
        self.statistics_button.clicked.connect(self.open_statistics_screen)

    def open_training_screen(self):
        self.training_window.set_cards(self.all_cards)
        self.training_window.reset_training()
        self.training_window.show()

    def open_statistics_screen(self):
        self.statistics_window.show()

    def open_create_cards_screen(self):
        self.create_cards_window.show()

    def update_list_cards_window(self):
        self.list_cards_window.populate_list()

class TrainingWindow(QMainWindow, Ui_TrainingWindow): # окно тренировки
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        self.cards = {}
        self.card_keys = []
        self.current_question = None
        self.current_answer = None
        self.answer_shown = False
        self.allow_change_statistic = False

        self.show_answer_button.clicked.connect(self.show_answer)  # подключение кнопок
        self.right_button.clicked.connect(self.show_next_question)
        self.not_right_button.clicked.connect(self.show_next_question)
        self.right_button.clicked.connect(self.count_true_answer)
        self.not_right_button.clicked.connect(self.count_false_answer)
        self.exit_button.clicked.connect(self.close_TrainingWindow)

    def set_cards(self, cards):
        self.cards = cards
        self.card_keys = list(self.cards.keys())
        self.reset_training()

    def reset_training(self):
        if self.card_keys:
            random.shuffle(self.card_keys)
            self.current_index = 0
            self.display_question()
            self.answer_shown = False

    def display_question(self):  # отображение вопроса
        if self.card_keys:
            self.current_question = self.card_keys[self.current_index]
            self.current_answer = self.cards[self.current_question]
            self.question_label.setText(self.current_question)
            self.answer_label.setText("")
        else:
            self.question_label.setText("Нет доступных карточек. Пожалуйста, добавьте карточки!")
            self.answer_label.setText("")
        self.show_answer_button.setEnabled(True)

    def show_answer(self):  # отображение ответа
        if self.current_answer and not self.answer_shown:
            self.answer_label.setText(self.current_answer)
            self.allow_change_statistic = True
            self.not_right_button.setEnabled(True)
            self.right_button.setEnabled(True)
            self.show_answer_button.setEnabled(False)
            self.answer_shown = True

    def count_true_answer(self):  # счётчик правильных ответов
        if self.allow_change_statistic:
            self.main_window.true_answer += 1
            self.not_right_button.setEnabled(False)
            self.right_button.setEnabled(False)
            self.allow_change_statistic = False

    def count_false_answer(self):  # счётчик неправильных ответов
        if self.allow_change_statistic:
            self.main_window.false_answer += 1
            self.not_right_button.setEnabled(False)
            self.right_button.setEnabled(False)
            self.allow_change_statistic = False

    def show_next_question(self):  # отображение следующей карточки
        if self.card_keys:
            self.current_index = (self.current_index + 1) % len(self.card_keys)
            self.display_question()
            self.answer_shown = False

    def close_TrainingWindow(self):
        self.close()


class CreatCardsWindow(QMainWindow, Ui_CreatCardsWindow): # Класс для создания карточек
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window

        self.exit_button.clicked.connect(self.close_CreatCardsWindow)  # подключение кнопок
        self.add_card_button.clicked.connect(self.creat_new_card)
        self.list_cards_button.clicked.connect(self.open_list_cards_window)

    def close_CreatCardsWindow(self):
        self.close()

    def open_list_cards_window(self):
        self.main_window.update_list_cards_window()
        self.main_window.list_cards_window.show()

    def creat_new_card(self):
        question_text = self.input_question_text.toPlainText()
        answer_text = self.input_answer_text.toPlainText()

        if not question_text or not answer_text:  # проверка на заполненость окна вопроса и окна ответа
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите вопрос и ответ.")
            return

        self.main_window.all_cards[question_text] = answer_text

        self.input_question_text.clear()
        self.input_answer_text.clear()



class ListCardsWindow(QMainWindow, Ui_ListCardsWindow): # Класс для отображения списка карточек
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        self.card_list_widget = self.findChild(QListWidget, 'list_all_cards_listwidget')

        self.exit_button.clicked.connect(self.close_ListCardsWindow)  # подключение кнопки

    def close_ListCardsWindow(self):
        self.close()

    def populate_list(self):  # вывод списка карточек на экран
        self.list_all_cards_listwidget.clear()
        for question, answer in self.main_window.all_cards.items():
            item_text = f"В: {question}\nО: {answer}"
            item = QListWidgetItem(item_text)
            self.card_list_widget.addItem(item)


class StatisticsWindow(QMainWindow, Ui_StatisticsWindow): # Класс для отображения статистики
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window

        self.exit_button.clicked.connect(self.close_StatisticsWindow)
        self.reset_statistics_button.clicked.connect(self.reset_statistics)  # подключение кнопок

    def show(self):
        self.update_statistics()
        super().show()

    def update_statistics(self):  # обновление статистики
        true_count = self.main_window.true_answer
        false_count = self.main_window.false_answer
        count_all_answer = self.main_window.true_answer + self.main_window.false_answer
        self.count_all_answer_label.setText(str(count_all_answer))
        self.counter_right_answer_label.setText(str(true_count))
        self.count_no_rights_answer_label.setText(str(false_count))

    def reset_statistics(self):  # сброс статистики
        self.main_window.false_answer = 0
        self.main_window.true_answer = 0
        self.update_statistics()

    def close_StatisticsWindow(self): # закрывает окно статистики
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
