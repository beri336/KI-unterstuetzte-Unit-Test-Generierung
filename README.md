# KI-unterstuetzte-Unit-Test-Generierung
Thesis.

<p>Deutsche Version</p>

<br>

- <span style="color:orange;font-weight:500">Looking for the english version? Look here: [README English](README_EN.md)</span>

<hr>

## Inhaltsverzeichnis

01. [Motivation](#motivation)
02. [Installation](#installation)
03. [Benutzung](#benutzung)
04. [Beispiel](#beispiel)
05. [Code](#code)
06. [Probleme](#probleme)
07. [Ollama](#ollama)
08. [Contributors](#contributors)
09. [Licence](#licence)
10. [Version](#version)

<hr><hr>

## 1. Motivation

- <p>Dieses Projekt wurde im Rahmen meiner Bachelorarbeit (Thesis) an der HFU Furtwangen erstellt. Das Ziel ist es, mittels verschiedenen AI-Modellen (Open-Source) festzustellen, welches Modell am Besten funktioniert und mit welchem Prompt die Modelle am Besten Tests erstellen können. Die Arbeit zielt darauf ab, Unit Tests mittels AI zu evaluieren, kann aber durch die Prompts manipuliert beziehungsweise andere Testarten herangezogen werden.</p>
- <p>Da Software immer komplexer, größer und unübersichtlicher wird, war meine Motivation, den Testprozess zu automatisieren. Durch die Entwicklung eines Tools mit Python habe ich versucht, diesem Schritt etwas näher zu kommen. Durch AI sind Neuerungen entstanden, die sich auch auf die Software-Entwicklung auswirken und den Testprozess erweitern und Software-Fehler weitesgehend weiter verringern können.</p>

<hr>

## 2. Installation
- Lade dieses GitHub-Repository herunter mit dem Befehl `git clone https://github.com/beri336/AI-Unit-Testing`
- Installiere alle Abhängigkeiten mit `pip install ollama psutil`
- öffne den Ordner in deiner IDE und führe es aus
    - oder mit `python main.py`
    - oder erstelle ein ausführbares Programm:

> für MacOS
- installiere py2app mit `pip install py2app`
- erstelle im Verzeichnis `setup.py` und füge folgendes ein:
```Python
from setuptools import setup

APP = ['main.py']
OPTIONS = {'argv_emulation': True}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```
- und erstelle nun aus dem setup.py die ausführbare App mit `python setup.py py2app`
- im `dist`-Ordner liegt nun die App

<br>

> für Windows und Linux
- installiere pyinstaller mit `pip install pyinstaller`
- erstelle ein ausführbares Programm mit `pyinstaller --onefile main.py`

<hr>

## 3. Benutzung
- führe das Programm aus, die GUI sieht in etwa so aus:

![GUI](Pictures/GUI.png)

- klicke auf den `Choose Folder` und wähle dein Python-Projekt aus
- falls du einen Ordner hast, wie bspw. eine virtuelle Entwicklungsumgebung venv, kann diese im `Choose Excluded Folder` ausgeschlossen werden
- falls ein "Prompt"{.md, .txt, .doc} vorhanden ist, wird sie automatisch in die TextArea eingefügt
    - falls keine vorhanden ist, kann sie manuell ausgewählt werden mit `Choose Prompt`
    - oder schreibe selbst den Prompt in die TextArea hinein
- wähle im `Select AI Model` das AI-Modell, mit dem der Unit Test erstellt werden soll
- klicke auf `Generate`, um die Test-Generierung zu starten

<hr>

## 4. Beispiel
> <span style="color:orange;font-weight:500">nach den Schritten aus [Benutzung](#benutzung), sieht das Programm wie folgt aus:</span>

![Starting Generation](<Pictures/Starting Generation.png>)

- es wurden insgesamt 5 Python-Files gefunden
- der Ordner `Project 1` wurde ausgewählt und der Unter-Ordner `Venv` wurde von der Generierung ausgeschlossen
- ein Prompt-File wurde gefunden und automatisch geladen
- `Deepseek-Coder-V2` wurde als AI-Modell ausgewählt

- oben links ist der Status-Label des Testprozesses
    - `Ready`: kein Testprozess am Laufen, die Test-Generierung kann gestartet werden
    - `Generating, please wait... (x/y)`: die Unit-Tests werden erstellt, wobei x für die aktuellen Anzahl der abgeschlossenen Tests darstellt, und y für die Anzahl der zu erstellenden Tests
    - `Done`: die Unit-Tests sind fertig generiert, und bei Bedarf können weitere erstellt werden
- oben rechts ist der Ollama-Status-Label
    - <span style="color:green;font-weight:500">Ollama Online</span> zeigt auf, dass Ollama läuft und auf die AI-Modelle zugegriffen werden kann
    - <span style="color:red;font-weight:500">Ollama Offline</span> zeigt, dass Ollama nicht läuft und kein AI-Modell zur Verfügung steht

<br>

![While Generating](<Pictures/While Generating.png>)

- während der Test-Generierung, zeigen die Klammer und der Laddebalken, wie weit der Test ist
- am Anfang dauert es etwas länger, da dass AI-Modell gestartet und angesprochen werden muss, und je nach Code-Zeilen und Komplexität, kann die Generierung länger dauern

<br>

![Done Generating](<Pictures/Done Generating.png>)

- die Generierung aller Tests sind abgeschlossen, der Status-Label zeigt `Done` auf und der Ladebalken wird auf Standard `0` zurückgesetzt

<br>

![Ollama Offline](<Pictures/Ollama Offline.png>)

- wenn `Ollama Offline` angezeigt wird, heißt es, dass Ollama auf deinem System nicht läuft
- öffne das Terminal und starte Ollama, alle 10 Sekunden überprüft das Programm, ob Ollama aktiv ist und zeigt dieses dann auf

<hr>

## 5. Code
> <span style="color:orange;font-weight:500">In diesem Abschnitt wird kurz erklärt, was die jeweiligen Funktionen machen</span>

> `terminal_debugging(...)`, `terminal_standard(...)` und `terminal_error(...)`
- zeigt print-Ausgaben farbig in der Konsole an

<br>

> `chose_folder()`
- öffnet einen `filedialog`, wobei der Benutzer seinen Ordner auswählen kann
- wenn prompt.[`"txt", "md", "doc"`] gefunden werden, wird sie ins Textfeld geladen

<br>

> `chose_exclude_folder()`
- wenn das Haupt-Verzeichnis gewählt wurde, wird der Ausschließen-Button klickbar, andernfalls bleibt es ausgegraut und nicht anklickbar
- nur Unter-Ordner des Haupt-Verzeichnisses können gewählt werden
- nur ein Unter-Ordner kann ausgewählt werden (zum Beispiel eine `Virtuelle Entwicklungsumgebung`)

<br>

> `chose_prompt_file()`
- wenn kein Prompt-File gefunden wurde, kann der Benutzer hiermit einen File auswählen

<br>

> `fetch_models()`
- nutzt das `subprocess`, um `ollama list` im Terminal auszuführen
- das Ergebnis wird nach dem Modell-Namen gefiltert, da nur der Name für das Programm notwendig ist
- wenn ein Cache von den Modell-Namen vorhanden ist, wird diese genutzt

<br>

> `on_model_select(...)`
- wenn der Benutzer ein AI-Modell aus der Liste auswählt, aktualisiert diese Funktionen die Variable und den `Generate`-Button

<br>

> `initialize_progress_bar(...)`
- wenn Python-Files gefunden werden, setzt diese Funktion die Gesamtanzahl auf 100% für den Ladebalken

<br>

> `update_progress_bar(...)`
- wenn ein Test von der Gesamtzahl abgeschlossen ist, aktualisiert diese Funktion den Ladebalken

<br>

> `reset_progress_bar()`
- wenn alle Tests abgeschlossen sind, setzt diese Funktion den Ladebalken auf 0 zurück

<br>

> `generate_tests()`
- wenn kein Modell ausgewählt wurde, wird der Testprozess nicht gestartet
- sucht nach allen `*.py`-Files im Ordner und speichert deren Pfad
- wenn keine Files gefunden werden, wird ein Error im Terminal angezeigt
- eröffnet einen neuen Thread und startet die Funktion `generate_tests_for_folder()`
- startet ebenfalls die Funktion `check_generation_completion()`

<br>

> `check_generation_completion()`
- überprüft jede Sekunde, ob der Thread aus `generate_tests()` läuft
- wenn nicht, sind alle Tests abgeschlossen und es startet die Funktion `show_done_label()`

<br>

> `show_done_label()`
- aktualisiert den Status-Label zu `Done` und setzt das Label zu `Ready` nach 5 Sekunden

<br>

> `generate_tests_for_folder(...)`
- erstellt einen `Tests`-Ordner im Haupt-Verzeichnis
- erstellt einen Log-File mit Unit-Test-Generierungsdetails
- für jedes einzelne Python-File wird `generate_test_for_file()` aufgerufen
- startet `reset_progress_bar()`

<br>

> `generate_test_for_file(...)`
- schickt jedes einzelne Python-File zum gewählten AI-Modell, fängt die Markdown-Abfrage ab und filtert sie nur nach dem Python-Code und entfernt den Rest
- fügt die Generierungszeit zum Log-File hinzu

<br>

> `check_ollama_status()`
- überprüft alle 10 Sekunden, ob Ollama noch aktiv ist

<br>

> Aufbau der `GUI`
- setzt `minsize` und `maxsize` zu den exakten X- und Y-Koordinaten, um die GUI zu fixieren
- erstellt ein Main-Frame
- erstellt innerhalb des Main-Frame weitere Unter-Frames:
    - `frame one` zeigt den Test-Status und Ollama-Status an
    - `frame two` zeigt den ausgewählten Haupt-Ordner
    - `frame three` zeigt den ausgeschlossenen Ordner innerhalb des Haupt-Ordners an
    - `frame four` zeigt den Prompt an
    - `frame five` zeigt alle auswählbaren AI-Modelle an
    - `frame six` zeigt den `Generate`-Button an
    - `frame seven` zeigt den Ladebalken

<hr>

## 6. Probleme
- Die Performance des Programms ist abhängig vom gewählten AI-Modell. In manchen Fällen kann der Testprozess einige Sekunden dauern, aber auch einige Minuten.
- Die Performance ist ebenfalls von gegebenen Code abhängig (einfach, komplex, nur ein paar Code-Zeilen oder meherere 1.000-Zeilen).
- Die Performance ist von System zu System unterschiedlich. Mit besseren GPU's ist die Generierung schneller.
- Da Fehler nicht ausgeschlossen sind, ist es ratsam, die generierten Unit-Tests nochmals anzuschauen. AI macht Fehler.

<hr>

## 7. Ollama
> Was ist Ollama?
- Ollama ist ein leichtgewichtiges Framework, dass es einem ermöglicht, große Sprachmodelle `Large Language Models [LLM]` lokal auf dem eigenen System auszuführen.
- Es bietet eine einfache API an, mit der zum Erstellen, Ausführen und Verwalten von Modellen genutzt werden kann.
- Zudem gibt es eine Bibliothek mit vorgefertigen und vortrainierten Modellen, die in verschiedenen Anwendungen eingesetzt werden kann.
- Mit Ollama können so Modelle wie LLama 3.2, Phi 3, Gemma 2 oder weitere genutzt und sogar eigene Modelle angepasst oder erstellt werden.
- Dieses Tool ist für alle gängigen Betriebssysteme (macOS, Linux, Windows) verfügbar und kann [hier](https://ollama.com/download) heruntergeladen werden.
- Durch die lokale Ausführung ist der rießen Vorteil, dass die persönlichen Daten nicht an Dritte gesendet werden.
- Ollama bietet zudem auch eine REST-API an, die die Integration in andere Anwendungen erleichtert.
- Auch sind offizielle Docker-Images von Ollama vorhanden, die die containerisierte Umgebung vereinfacht.
- Es bietet zudem Bibliotheken in Programmiersprachen an, sodass sie einfach in den Programm-Code integriert werden können, [hier beispielsweise für Python auf GitHub](https://github.com/ollama/ollama-python).

<br>

> Wie kann ich Ollama herunterladen?
- Gehe auf die [offizielle Homepage von Ollama](https://ollama.com) oder hier direkt zur [Download-Webseite](https://ollama.com/download).
- Installiere Ollama nun für dein Betriebssystem.

<br>

> Wie kann ich mit Ollama AI-Modelle herunterladen?
- Einfacher können Modelle nicht sein.
- Gehe auf die [offizielle Ollama Modell Liste](https://ollama.com/search) und suche dir dein AI-Modell aus.
- In diesem Projekt wurden folgende Modelle genutzt:
    - [LLama3.2](https://ollama.com/library/llama3.2:3b)
    - [Gemma2](https://ollama.com/library/gemma2:9b)
    - [Deepseek Coder V2](https://ollama.com/library/deepseek-coder-v2:16b)
    - [CodeGemma](https://ollama.com/library/codegemma:7b)

<br>

> Quick Tour durch Ollama
- <span style="color:orange;font-weight:500">Alle folgenden Befehle müssen im Terminal ausgeführt werden.</span>

>> AI-Modelle herunterladen: `ollama pull {dein-ai-modell}`
>>> wenn du eine spezielle Variante runterladen willst (Parameter): `ollama pull {dein-ai-modell}:{parameter}`

>> AI-Modell starten: `ollama run {dein-ai-modell}`

>> Zeige alle heruntergeladenen AI-Modelle: `ollama list`

>> Zeige Informationen über das AI-Modell an: `ollama show {dein-ai-modell}`

>> Ollama starten: `ollama serve`

>> AI-Modell beenden: `ollama stop {dein-ai-modell}`

>> Zeige alle aktuell laufenden AI-Modelle: `ollama ps`

>> Für mehr: `ollama --help`

<hr>

## Contributors
- Berkant Simsek (Ersteller des Programms)

<hr>

## Licence
- MIT Licence

<hr>

## Version
> `V1.0`
- Automatisierte Unit-Tests-Erstellung mit AI.

<hr>