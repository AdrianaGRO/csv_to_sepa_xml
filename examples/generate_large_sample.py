#!/usr/bin/env python3
"""
Generate a large sample CSV file with 10,000 valid SEPA payments for load testing.
"""

import random
import csv

# Sample data pools
first_names = [
    "Maria", "Hans", "Sophie", "Lukas", "Emma", "Felix", "Anna", "Maximilian",
    "Laura", "Paul", "Julia", "Leon", "Lena", "Jonas", "Sarah", "Elias",
    "Lisa", "Noah", "Mia", "Ben", "Clara", "Finn", "Lea", "Alexander",
    "Giovanni", "Francesco", "Giuseppe", "Antonio", "Marco", "Alessandro",
    "Jean", "Pierre", "Michel", "Philippe", "Alain", "Jacques", "Francois",
    "Carlos", "Juan", "Jose", "Antonio", "Manuel", "Francisco", "David",
    "John", "James", "Robert", "Michael", "William", "David", "Richard",
    "Andrei", "Alexandru", "Mihai", "Ion", "Cristian", "Adrian", "Marian",
    "Elena", "Ana", "Ioana", "Andreea", "Gabriela", "Daniela", "Alina"
]

last_names = [
    "Schmidt", "Mueller", "Schneider", "Fischer", "Weber", "Meyer", "Wagner",
    "Becker", "Schulz", "Hoffmann", "Schaefer", "Koch", "Richter", "Klein",
    "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo",
    "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Petit", "Durand",
    "Garcia", "Rodriguez", "Martinez", "Lopez", "Gonzalez", "Hernandez",
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis",
    "Popescu", "Ionescu", "Popa", "Gheorghiu", "Constantinescu", "Stan",
    "Dumitrescu", "Stoica", "Marin", "Tudor", "Barbu", "Moldovan"
]

companies = [
    "GmbH", "AG", "KG", "Consulting", "Services", "Solutions", "Group",
    "International", "Systems", "Technologies", "Industries", "Trading",
    "Partners", "Enterprises", "Corporation", "Holdings", "Logistics"
]

# Valid IBANs for different countries with correct checksums
sample_ibans = {
    'DE': [  # Germany - 22 chars
        "DE89370400440532013000",
        "DE44500105175407324931",
        "DE27100777770209299700",
        "DE62370400440532013001",
        "DE91100000000123456789",
    ],
    'FR': [  # France - 27 chars
        "FR7630006000011234567890189",
        "FR1420041010050500013M02606",
        "FR7612548029989876543210843",
    ],
    'IT': [  # Italy - 27 chars
        "IT60X0542811101000000123456",
        "IT40S0542811101000000123456",
        "IT28W8000000292100645211111",
    ],
    'ES': [  # Spain - 24 chars
        "ES9121000418450200051332",
        "ES7921000813610123456789",
        "ES1000492352082414205416",
    ],
    'NL': [  # Netherlands - 18 chars
        "NL91ABNA0417164300",
        "NL02ABNA0123456789",
    ],
    'BE': [  # Belgium - 16 chars
        "BE68539007547034",
        "BE71096123456769",
    ],
    'AT': [  # Austria - 20 chars
        "AT611904300234573201",
        "AT483200000012345864",
    ],
    'CH': [  # Switzerland - 21 chars
        "CH9300762011623852957",
        "CH5604835012345678009",
    ],
    'RO': [  # Romania - 24 chars
        "RO49AAAA1B31007593840000",
        "RO09BCYP0000001234567890",
        "RO66BRDE410SV38975310410",
        "RO76BTRL01304205R50067XX",
    ],
}

# BICs for each country
sample_bics = {
    'DE': ["COBADEFFXXX", "INGDDEFFXXX", "DEUTDEFFXXX", "BYLADEM1XXX", "DRESDEFF100"],
    'FR': ["BNPAFRPPXXX", "AGRIFRPPXXX", "CRLYFRPPXXX", "SOGEFRPPXXX", "CEPAFRPP415"],
    'IT': ["BPPIITRRXXX", "UNCRITMM", "BCITITMM", "INTESA", "BLOPIT22XXX"],
    'ES': ["CAIXESBBXXX", "BBVAESMM", "BSCHESMM", "SABSESMMXXX", "POPUESMM"],
    'NL': ["ABNANL2AXXX", "RABONL2UXXX", "INGBNL2AXXX", "TRIONL2UXXX"],
    'BE': ["GKCCBEBB", "KREDBEBB", "GEBABEBB", "AXABBE22XXX"],
    'AT': ["BKAUATWWXXX", "GIBAATWWXXX", "RLNWATWWXXX"],
    'CH': ["UBSWCHZHXXX", "CRESCHZZXXX", "POFICHBEXXX"],
    'RO': ["RNCBROBU", "BTRLRO22XXX", "BRDEROBUXXX", "BCYPROBUXXX", "INGBROBU"],
}

references = [
    "Invoice", "Contract", "Payment", "Salary", "Consulting", "Services",
    "Order", "Commission", "Bonus", "Refund", "Credit Note", "Advance",
    "Retainer", "Fee", "Subscription", "License", "Maintenance", "Support"
]

streets = [
    "Main Street", "High Street", "Church Road", "Station Road", "Park Avenue",
    "Victoria Street", "Green Lane", "Manor Road", "Church Street", "Park Road",
    "Hauptstrasse", "Bahnhofstrasse", "Gartenstrasse", "Schulstrasse", "Kirchweg",
    "Via Roma", "Via Milano", "Corso Italia", "Via Nazionale", "Piazza Garibaldi",
    "Rue de la Paix", "Avenue des Champs", "Boulevard Victor Hugo", "Rue du Commerce",
    "Calle Mayor", "Avenida Principal", "Plaza de España", "Calle Real",
    "Strada Principala", "Bulevardul Unirii", "Calea Victoriei"
]

cities = [
    "Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Stuttgart", "Dresden",
    "Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Bordeaux", "Lille",
    "Rome", "Milan", "Naples", "Turin", "Florence", "Venice", "Bologna",
    "Madrid", "Barcelona", "Valencia", "Seville", "Bilbao", "Malaga",
    "Amsterdam", "Rotterdam", "Utrecht", "Eindhoven", "Brussels", "Antwerp",
    "Vienna", "Salzburg", "Zurich", "Geneva", "Bucharest", "Cluj-Napoca"
]

stores = [
    "Aldi", "Lidl", "Rewe", "Edeka", "Kaufland", "Real", "Penny",
    "Carrefour", "Leclerc", "Auchan", "Casino", "Monoprix",
    "Coop", "Esselunga", "Conad", "Carrefour Italia",
    "Mercadona", "Dia", "Alcampo", "El Corte Inglés",
    "Albert Heijn", "Jumbo", "Plus", "Spar",
    "Migros", "Coop Schweiz", "Denner",
    "Kaufland Romania", "Carrefour Romania", "Mega Image"
]

def generate_name():
    """Generate a random person or company name."""
    if random.random() < 0.7:  # 70% persons
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    else:  # 30% companies
        return f"{random.choice(last_names)} {random.choice(companies)}"

def generate_payment():
    """Generate one valid payment row."""
    # Pick a random country
    country = random.choice(list(sample_ibans.keys()))
    
    # Get valid IBAN and BIC for that country
    iban = random.choice(sample_ibans[country])
    bic = random.choice(sample_bics[country])
    
    # Generate random amount between 50 and 50,000 euros
    amount = round(random.uniform(50.0, 50000.0), 2)
    
    # Generate reference
    ref_type = random.choice(references)
    ref_number = random.randint(2024001, 2026999)
    reference = f"{ref_type} {ref_number}"
    
    # Generate address
    street_number = random.randint(1, 999)
    street = random.choice(streets)
    city = random.choice(cities)
    postal_code = random.randint(10000, 99999)
    address = f"{street} {street_number}, {postal_code} {city}"
    
    # Pick a favorite store
    favorite_store = random.choice(stores)
    
    return {
        'name': generate_name(),
        'iban': iban,
        'bic': bic,
        'amount': f"{amount:.2f}",
        'reference': reference,
        'address': address,
        'favorite_store': favorite_store
    }

def main():
    """Generate CSV file with 10,000 payments."""
    num_payments = 10000
    filename = "sample_payments_10k.csv"
    
    print(f"Generating {num_payments:,} sample payments...")
    
    payments = []
    for i in range(num_payments):
        payments.append(generate_payment())
        if (i + 1) % 1000 == 0:
            print(f"  Generated {i + 1:,} payments...")
    
    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'iban', 'bic', 'amount', 'reference', 'address', 'favorite_store'])
        writer.writeheader()
        writer.writerows(payments)
    
    # Calculate total
    total_amount = sum(float(p['amount']) for p in payments)
    
    print(f"\n✅ Created {filename}")
    print(f"   Payments: {num_payments:,}")
    print(f"   Total amount: EUR {total_amount:,.2f}")
    print(f"\nTest the converter:")
    print(f"   python3 -m csv_to_sepa_xml.main --cli {filename} output_10k.xml")

if __name__ == "__main__":
    main()
