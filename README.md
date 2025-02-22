# KI-unterstützte Unit-Test-Generierung
Thesis-Projekt für automatisierte Unit-Test-Generierung mit KI.

<p>Deutsche Version</p>

<br>

📌 Looking for the **[English Version](README_EN.md)**?

<hr>

## Inhaltsverzeichnis

1. [Motivation](#1-motivation)
2. [Installation](#2-installation)
3. [Benutzung](#3-benutzung)
4. [Code](#4-code)
5. [Ollama](#5-ollama)
6. [Contributors](#6-contributors)
7. [Licence](#7-licence)
8. [Version](#8-version)

<hr><hr>

## 1. Motivation

Dieses Projekt entstand im Rahmen meiner **Bachelorarbeit an der HFU Furtwangen**. Ziel ist es, verschiedene **Open-Source-KI-Modelle** zu testen, um herauszufinden, welches Modell sich am besten für die automatische **Unit-Test-Generierung** eignet.

> **Warum?**  
- Software wächst rasant, Tests sind zeitaufwändig.  
- KI kann den **Testprozess beschleunigen & automatisieren**.  
- Modelle können mit speziellen **Prompts** gezielt für Tests optimiert werden.

Dieses Tool wurde mit **Python & CustomTkinter** entwickelt und nutzt **lokale LLMs über Ollama**, um Tests effizient zu generieren.

<hr>

## 2. Installation

### **Projekt klonen & Abhängigkeiten installieren:**
```bash
git clone https://github.com/beri336/KI-unterstuetzte-Unit-Test-Generierung
cd KI-unterstuetzte-Unit-Test-Generierung
pip install -r requirements.txt
```

### **Manuelle Installation der Bibliotheken:**
```bash
pip install customtkinter ollama psutil
```

<hr>

## 3. Benutzung

**GUI-Ansicht:**  
![GUI](Pictures/GUI.png)


### **Schritt-für-Schritt Anleitung**
1. **Projektordner wählen** -> `Choose Folder`.  
2. **(Optional) Ausschlussordner wählen** -> `Choose Excluded Folder` (z. B. virtuelle Umgebung).  
3. **Prompt-Datei laden** (falls `prompt.{md, txt, doc}` im Ordner liegt, wird sie automatisch erkannt).  
   - Falls keine vorhanden ist, kann eine mit `Choose Prompt` manuell ausgewählt oder direkt ins Textfeld eingegeben werden.  
4. **KI-Modell wählen** -> `Select AI Model`.  
5. **Optionen setzen**:  
   - `Save Raw Markdown`: Speichert die komplette KI-Antwort.  
   - `Create Log-File`: Erstellt eine Log-Datei zur Dokumentation.  
6. **Generierung starten** -> `Generate`.  

<hr>

## 4. Code

### **Hilfsfunktionen**
> `output_terminal(...)`
- Zeigt farbige Debugging-Meldungen im Terminal an.

> `set_status_label(...)`
- Aktualisiert das Status-Label in der GUI.

> `set_generate_label(...)`
- Aktualisiert das Generierungsstatus-Label.

> `set_ollama_label(...)`
- Setzt das Ollama-Status-Label basierend auf dem Verbindungsstatus.

<br>

### **Testgenerierung**
> `generate_tests()`
- Startet die Testgenerierung und deaktiviert UI-Elemente.

> `generate_tests_for_folder(...)`
- Erstellt Tests für alle gefundenen Python-Dateien.

> `generate_test_for_file(...)`
- Generiert einen Unit-Test für eine einzelne Datei.

> `extract_python_code(...)`
- Filtert nur den Python-Code aus der KI-Antwort.

> `save_files(...)`
- Speichert die generierten Tests und optional eine Markdown-Datei.

<br>

### **Progress & Status Updates**
> `initialize_progress_bar(...)`
- Setzt den Fortschrittsbalken auf 0%.

> `update_progress_bar(...)`
- Aktualisiert den Fortschrittsbalken basierend auf dem Fortschritt.

> `reset_progress_bar()`
- Setzt den Fortschrittsbalken zurück.

> `check_generation_completion()`
- Überwacht den Fortschritt der Testgenerierung.

<br>

### **Modell & KI-Interaktion**
> `fetch_models()`
- Lädt verfügbare KI-Modelle per `ollama list`.

> `on_model_select(...)`
- Aktualisiert das gewählte KI-Modell und den `Generate`-Button.

> `check_ollama_status()`
- Überprüft regelmäßig, ob Ollama aktiv ist.

<br>

### **Datei- und Ordnerauswahl**
> `choose_folder()`
- Öffnet einen Dialog zur Auswahl des Projektordners.

> `choose_exclude_folder()`
- Erlaubt das Ausschließen eines Unterordners.

> `choose_prompt_file()`
- Ermöglicht das manuelle Laden einer Prompt-Datei.

<br>

### **GUI**
> `setup_gui()`
- Erstellt das Hauptfenster der Anwendung mit CustomTkinter.
- Organisiert die GUI in mehrere Frames für eine saubere Struktur:
  - **Frame 1**: Statusanzeigen für Test- und Ollama-Status.
  - **Frame 2**: Auswahl des Hauptordners.
  - **Frame 3**: Ausschluss eines Unterordners.
  - **Frame 4**: Anzeige der Prompt-Datei.
  - **Frame 5**: Dropdown für die Modell-Auswahl.
  - **Frame 6**: `Generate`-Button.
  - **Frame 7**: Fortschrittsbalken.

<hr>

## 5. Ollama
### **Was ist Ollama?**
- Leichtgewichtiges Framework für lokale **Large Language Models (LLMs)**.
- Unterstützt Modelle wie **LLama 3, Phi 3, Gemma 2**.
- **Vorteile:** Kein Cloud-Upload, volle Kontrolle, Open-Source.
- [Offizielle Webseite](https://ollama.com)

### **Installation & Nutzung**
```bash
# Installieren
ollama pull {modellname}

# Verfügbare Modelle anzeigen
ollama list

# Modell starten
ollama run {modellname}

# Modell stoppen
ollama stop {modellname}

# Modell-Details anzeigen
ollama show {modellname}
```

### **Beispiel:**
```bash
ollama pull llama3
ollama run llama3
```

<hr>

## 6. Contributors
- **Berkant Simsek**

<hr>

## 7. Licence
- **MIT Licence**

<hr>

## 8. Version
> V1.0 von GenUnit
- **Automatisierte Unit-Tests-Erstellung mit KI.**

<hr>