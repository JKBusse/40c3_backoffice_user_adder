# Assembly-Mitglieder hinzufügen

Kleine Flask-Anwendung, mit der sich per Eingabe von Benutzernamen Mitglieder zu einer Assembly im
40C3-Hub hinzufügen lassen.

Die öffentliche API (`api.events.ccc.de`) bietet keinen Endpoint dafür. Die App meldet sich deshalb
mit einem Hub-Account im Backoffice an und schickt dasselbe Formular ab wie
"Mitglied hinzufügen" auf der Members-Seite der Assembly.

## Konfiguration

```sh
cp .env.example .env
```

| Variable        | Bedeutung                                                              |
| --------------- | ---------------------------------------------------------------------- |
| `ASSEMBLY_ID`   | UUID der Assembly (steht in der Backoffice-URL `.../assembly/<id>/members`) |
| `HUB_USER`      | Benutzername oder E-Mail des Hub-Accounts                              |
| `HUB_PASSWORD`  | Passwort des Accounts                                                  |
| `SECRET_KEY`    | Schlüssel für Flask-Sessions, z. B. `python3 -c "import secrets; print(secrets.token_hex(32))"` |

Der Account muss die Assembly verwalten dürfen. Ist 2FA aktiv, funktioniert der Login nicht.

## Starten

Mit Docker Compose:

```sh
docker compose up --build
```

Lokal:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Die App ist dann unter http://localhost:8000 (Docker) bzw. http://127.0.0.1:5000 (lokal) erreichbar.

## Verwendung

Einen oder mehrere Benutzernamen eingeben (einer pro Zeile oder kommagetrennt) und absenden.

Die Meldung "Anfrage gesendet" bedeutet nur, dass das Backoffice die Anfrage angenommen hat. Ob der
Benutzer tatsächlich hinzugefügt wurde (z. B. bei unbekanntem Namen), wird nicht geprüft.
