from src.app import *
#app.run(debug=True)

import streamlit as st

"""
# Sprich mit der AI
[Openai](https://openai.com/blog/better-language-models/) hat Anfang dieses Jahres für Aufsehen gesorgt.
Sie veröffentlichten ein Paper in welchen sie beschreiben, wie sie eine Sprach AI mit rund 
40 GB Texten trainierten. Das besondere die AI lieferte Texte in einer qualität, welche nur schwer von 
Menschen geschreiben Texten unterscheiden lässt. Normalerweise veröffentlicht Openai gleichzeitig den Code und das Modell. Doch 
dieses mal war es anders. Sie veröffentlichten nur ein stark reduziertes Modell mit dem Hinweis, dass es 
für falsche Zwecke verwendet werden könnte. Z.B. könnten mit ein solchen AI einfach Fakenews oder Spam generiert werden.
Am 05. November 2019 veröffentlichte Openai nun das volle Modell.

Weiter unten können sie sich selbst von der Qualtität der Texte überzeugen. Da die AI nur englisch versteht, übersetzen wir 
mit Hilfe von Azure-Translate (eine Übersetzungs AI) die Texte in English und wieder zurück. Probieren sie es selbst.

Das Modell ist sehr rechenintensiv. Deshalb nehmen sie sich etwas Zeit bis die Antwort erscheint. 
"""

text_input = ""
text_input = st.text_input('hier können Sie einen Beispieltext eingeben', '')


if text_input != "":
    todo = TodoDAO()
    text_output = todo.get_ai_text(text_input)
    st.write(text_output)