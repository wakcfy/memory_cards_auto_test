import pytest
from PyQt5.QtWidgets import QApplication
from memory_cards import MainWindow, TrainingWindow, CreatCardsWindow, ListCardsWindow, StatisticsWindow


@pytest.fixture(scope="session")
def qapp():
    app = QApplication([])
    yield app

@pytest.fixture
def main_window(qapp):
    window = MainWindow()
    yield window

@pytest.fixture
def training_window(main_window):
    window = TrainingWindow(main_window)
    yield window

@pytest.fixture
def create_cards_window(main_window):
    window = CreatCardsWindow(main_window)
    yield window

@pytest.fixture
def list_cards_window(main_window):
    window = ListCardsWindow(main_window)
    yield window

@pytest.fixture
def statistics_window(main_window):
    window = StatisticsWindow(main_window)
    yield window


def test_main_window_initialization(main_window):
    assert main_window.true_answer == 0
    assert main_window.false_answer == 0
    assert main_window.all_cards == {}

def test_main_window_open_training_screen(main_window, mocker):
    mocker.patch.object(main_window.training_window, 'show')
    main_window.open_training_screen()
    main_window.training_window.show.assert_called_once()


def test_training_window_initialization(training_window):
    assert training_window.cards == {}
    assert training_window.card_keys == []
    assert training_window.current_question is None
    assert training_window.current_answer is None
    assert training_window.answer_shown is False

def test_training_window_set_cards(training_window):
    cards = {"question1": "answer1", "question2": "answer2"}
    training_window.set_cards(cards)
    assert training_window.cards == cards
    assert list(training_window.cards.keys()) == ["question1", "question2"]

def test_training_window_reset_training(training_window):
    cards = {"question1": "answer1", "question2": "answer2"}
    training_window.set_cards(cards)
    training_window.reset_training()
    assert training_window.current_question is not None
    assert training_window.answer_shown is False


def test_create_cards_window_initialization(create_cards_window):
    assert create_cards_window.main_window is not None

def test_create_cards_window_create_new_card(create_cards_window, main_window, mocker):
    mocker.patch.object(create_cards_window.input_question_text, 'toPlainText', return_value="question")
    mocker.patch.object(create_cards_window.input_answer_text, 'toPlainText', return_value="answer")
    create_cards_window.creat_new_card()
    assert "question" in main_window.all_cards
    assert main_window.all_cards["question"] == "answer"

def test_list_cards_window_initialization(list_cards_window):
    assert list_cards_window.main_window is not None

def test_list_cards_window_populate_list(list_cards_window, main_window):
    main_window.all_cards = {"question1": "answer1", "question2": "answer2"}
    list_cards_window.populate_list()
    assert list_cards_window.card_list_widget.count() == 2

def test_statistics_window_initialization(statistics_window):
    assert statistics_window.main_window is not None

def test_statistics_window_update_statistics(statistics_window, main_window):
    main_window.true_answer = 5
    main_window.false_answer = 2
    statistics_window.update_statistics()
    assert statistics_window.count_all_answer_label.text() == "7"
    assert statistics_window.counter_right_answer_label.text() == "5"
    assert statistics_window.count_no_rights_answer_label.text() == "2"

def test_statistics_window_reset_statistics(statistics_window, main_window):
    main_window.true_answer = 5
    main_window.false_answer = 2
    statistics_window.reset_statistics()
    assert main_window.true_answer == 0
    assert main_window.false_answer == 0
    statistics_window.update_statistics()
    assert statistics_window.count_all_answer_label.text() == "0"
    assert statistics_window.counter_right_answer_label.text() == "0"
    assert statistics_window.count_no_rights_answer_label.text() == "0"
