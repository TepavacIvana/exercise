# import pytest
#
#
# class Notes:
#     def __init__(self):
#         self.title_values = {}
#         self.note_values = {}
#         self.user_id_values = {}
#
#     def add(self, title, title_value, note, note_value, user_id, user_id_value):
#         self.title_values[title] = title_value
#         self.note_values[note] = note_value
#         self.user_id_values[user_id] = user_id_value
#
#     def lookup(self, title, note, user_id):
#         return self.title_values[title], self.note_values[note], self.user_id_values[user_id]
#
#     def update(self, title, title_value):
#         self.title_values[title] = title_value
#
#     def clear(self):
#         print(self)
#
#
# @pytest.fixture
# def notes():
#     return Notes()
#
#
# def test_create_note(notes):
#     notes.add('title', 'Naziv', 'note', 'Dugacka poruka', 'user_id', 6)
#     assert ('Naziv', 'Dugacka poruka', 6) == notes.lookup('title', 'note', 'user_id')
#
#
# def test_validate_if_longer_or_forbidden(notes):
#     notes.add('title', 'Naziv', 'note', 'impossible', 'user_id', 6)
#     forbidden_words = ['unbelievable', 'impossible', 'undoable', 'can not', 'would not']
#
#     tv = notes.title_values['title']
#     nv = notes.note_values['note']
#
#     assert len(tv) <= 20
#     assert forbidden_words[0] not in nv
#
#
# def test_listing(notes):
#     notes.add('title', 'Titl', 'note', 'Kratka poruka', 'user_id', 3)
#     assert (None, None, None) != notes.lookup('title', 'note', 'user_id')
#
#
# def test_single_note(notes):
#     notes.add('title', None, 'note', None, 'user_id', 1)
#     assert notes.user_id_values['user_id'] is not None
#
#
# def test_missing_note_raises_error(notes):
#     with pytest.raises(KeyError):
#         notes.lookup('title', 'note', 'user_id')
#
#
# def test_update(notes):
#     notes.add('title', 'Titl', 'note', 'Kratka poruka', 'user_id', 3)
#     notes.update('title', 'Nisam titl')
#     assert ('Titl', 'Kratka poruka', 3) != notes.lookup('title', 'note', 'user_id')
#
#
# def test_update2(notes):
#     notes.update('title', 'Nisam titl')
#     assert notes.title_values['title'] is not None
#
#
# def test_update_missing_note(notes):
#     with pytest.raises(KeyError):
#         notes.update('name', 'Ivana')
#         notes.lookup('title', 'note', 'user_id')
#
#
# def test_delete(notes):
#     notes.add('title', 'Titl', 'note', 'Neka poruka za brisanje', 'user_id', 3)
#     # #     # nv = notes.note_values['note']
#     notes.clear()
#     assert notes == {}
