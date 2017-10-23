# fa2909

Readme Datei

############################################################################
# Installation unter Windows
############################################################################

Für die Installation unter Windows wird empfohlem Miniconda zu verwenden.
Miniconda ist eine open source Python Distribution und ist speziell zur Datenverarbeitung, Prädiktiven Analyse und Maschinellem Lernen geeignet.
Miniconda vereinfacht die Paketverwaltung von Modulen und erleichter somit die Installation und Weiterverbreitung von Software in Python.
Miniconda kann unter https://conda.io/miniconda.html heruntergeladen werden.

Nach der Installation müssen über die Anaconda Prompt alle von dem Prototyp verwendeten Module installiert werden:

	conda install matplotlib
	conda install scikit-learn
	conda install pyqt=4
	conda install -c anaconda Django
	conda install -c conda-forge djangorestframework
	conda install -c anaconda psycopg2

Anschließend kann die Applikation über die Anaconda Prompt oder über die Eingabeaufforderung gestartet werden:

python pfad/zum/projektordner/main.py




############################################################################
# Installation unter Linux
############################################################################

Für die Installation unter Linux liegt dem Projekt das Installationsskript install.sh bei.
Durch Ausführen des Skripts über das Terminal werden nach Eingabe des root Passworts automatisch alle notwendigen Abhängigkeiten installiert.

	sudo pfad/zum/projektordner/install.sh

Alternativ können die Module auch manuell installiert werden.
Dazu wird zur einfacheren Installation der notwendigen Module zuerst das Paketverwaltungsprogramm pip installiert und anschließend auf die aktuellste Version gebracht.

	sudo apt-get install python-pip
	sudo pip update --pip

Anschließend werden über pip nacheinander alle notwendigen Module installiert.

	sudo pip install psycopg2
	sudo pip install pyqtgraph
	sudo pip install matplotlib
	sudo pip install psycopg2
	sudo pip install djangorestframework

Da PyQt4 nicht im Repository von pip verfügbar ist wird dieses zusammen mit allen benötigten Abhängigkeiten aus dem Repository von Ubuntu installiert.

	sudo apt-get install python-qt4
	sudo apt-get install python-dev libpq-dev