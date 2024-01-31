from django.shortcuts import render, redirect
from .melody_randomizer import Melody_combs, Chords_progr, Arpeggio, Keychanger

from django.http import JsonResponse
from midiutil.MidiFile import MIDIFile
from midi_handler import *

def generate_melody(request):
    # Пример использования
    midi_handler = MidiHandler()
    midi_handler.add_track_name("Sample Track")
    midi_handler.add_tempo(120)
    # Вызов функции note_randomizer
    midi_handler = note_randomizer(midi_handler, tempo=120, start_time=0, end_time=180)
    # Добавление нот и т.д.
    midi_handler.save_midi("output.mid")

    # Здесь вы можете обработать результаты и вернуть их
    return JsonResponse({'status': 'success', 'data': 'Мелодия сгенерирована'})
