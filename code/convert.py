#!/usr/bin/env python3

# Simple script that enables views over tabs and basic operations over guitar tabs.

#  import sys
import re

def is_empty_line(line):
    return len(line) == 0

def get_property_line(line):
    split = line.index(':')
    return (line[:split].strip(),line[split+1:].strip())

def starts_with_heading(line):
    return line[0] == '['

def get_part_heading(line):
    begbr = line.index('[')
    endbr = line.index(']')
    name = line[begbr+1:endbr]
    return (name,line[endbr+1:].strip())

def is_chord_line(line):
    copy = line[:]
    orig_len = len(copy)
    copy = re.sub('[A-Gm0-9 ]', '', copy)
    new_len = len(copy)
    return new_len < orig_len/2

def new_nonempty_line():
    line = None
    while True:
        line = input()
        if not is_empty_line(line):
            break
    return line

class Part:
    def __init__(self, name):
        self.name = name
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

class Song:
    def __init__(self):
        self.properties = {}
        self.parts = []

    def add_property(self, key, value):
        self.properties[key] = value

    def add_part(self, name, optional_chords):
        # todo optional_chords
        self.parts.append(Part(name))

    def add_line(self, line):
        self.parts[-1].add_line(line)

def is_link(line):
    return line[:4] == 'http'

def make_link(name, link):
    return f'<a href={link}>{name}</a>'

def make_property(name, value):
    return f'<span>{name}: {value}</span>'

def song_to_html(song):
    html_string = []
    html_string.append('<html>')
    html_string.append('<ul>')
    for (k,p) in song.properties.items():
        html_string.append('<li>')
        if is_link(p):
            html_string.append(make_link(k,p))
        else:
            html_string.append(make_property(k,p))
        html_string.append('</li>')
    html_string.append('</ul>')
    html_string.append('<pre>')
    for part in song.parts:
        html_string.append(f'[{part.name}]')
        for line in part.lines:
            html_string.append(f'{line}')
    html_string.append('</pre>')
    html_string.append('</html>')
    return '\n'.join(html_string)

def parse_song_from_tab():
    song = Song()
    try:
        # process properties until newline
        while True:
            line = input()
            if is_empty_line(line):
                break
            (key, value) = get_property_line(line)
            song.add_property(key, value)
        # process song parts (verse, chorus, etc.)
        line = new_nonempty_line()
        while True:
            (name, optional_chords) = get_part_heading(line)
            song.add_part(name, optional_chords)
            # process part text
            while True:
                line = new_nonempty_line()
                if starts_with_heading(line):
                    break
                if is_chord_line(line):
                    # todo preprocess chords
                    song.add_line(line)
                else:
                    song.add_line(line)
    except EOFError:
        pass
    return song

def main():
    song = parse_song_from_tab()
    print(song_to_html(song))

if __name__ == '__main__':
    main()
