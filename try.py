import time
import json

def open_dagboek():
    # Functie om te controleren of de datum al bestaat in het dagboek
    def check_if_date_exists(date):
        try:
            with open('dagboek.json', 'r') as file:
                data = json.load(file)
                return date in data
        except FileNotFoundError:
            return False

    # Functie om tekst toe te voegen of te herschrijven in het dagboek
    def add_or_rewrite_entry(date, text, append=False):
        try:
            with open('dagboek.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        # voegt de nieuwe tekst toe aan bestaande tekst als append true is
        if append and date in data:
            data[date] += (" " + text)  # voegt een spatie en de tekst toe
        else:
            data[date] = text # voegt de nieuwe tekst toe

        with open('dagboek.json', 'w') as file:
            json.dump(data, file, indent=4) # zorgt ervoor dat het overzichtelijker is, binnen het json bestand

    # functie voor de dagboek invoer van de gebruiker
    def diary_entry():
        # vraagt de gebruiker om de datum en of de gebruiker iets zou willen toevoegen/herschrijven
        time.sleep(1)
        date_input = input("Wat is de datum vandaag, of welke datum zou u willen herschrijven/toevoegen? Gebruik het volgende formaat: DD-MM-YYYY: ")
        time.sleep(1)

        # controleert of de datum al bestaat
        if check_if_date_exists(date_input):
            user_choice = input("Deze datum is al ingevuld. Wil je de tekst herschrijven of toevoegen? (herschrijven/toevoegen): ").lower()
            time.sleep(1)
            if user_choice == 'herschrijven': # als de gebruiker wilt herschijven wordt er gevraagd de nieuwe tekst toe te voegen. Dit met de functie add_or_rewrite_entry
                new_text = input("Voer de nieuwe tekst in: ")
                time.sleep(1)
                add_or_rewrite_entry(date_input, new_text)
                print("De tekst is herschreven")
            elif user_choice == 'toevoegen':
                additional_text = input("Voer uw tekst in: ")
                time.sleep(1)
                add_or_rewrite_entry(date_input, additional_text, append=True)
                print("De tekst is toegevoegd")
                time.sleep(1)
        else:
            text = input("Deze dag is nog niet ingevuld. Voer uw tekst in: ") # als de datum niet in het json bestond is gevonden. Wordt er gevraagd de tekst toe te voegen.
            time.sleep(1)
            add_or_rewrite_entry(date_input, text)
            print("De tekst is toegevoegd")
            time.sleep(1)

    # het start van de code/functie dagboek
    diary_entry()
