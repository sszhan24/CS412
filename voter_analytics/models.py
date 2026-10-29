#models.py
#Sion Zhan (sszhan24@bu.edu), 10/27/26
#models for the voter_analytics application

from django.db import models
from datetime import datetime

# Create your models here.

class Voter(models.Model):
    """Store/represent the data for one registered voter in Newton, MA"""

    #identification
    voter_id = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()

    #address
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True)
    zip_code = models.TextField()

    #dates, using DateField for proper date handling
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()

    #political data
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.TextField()

    #voting history, True if they voted, False if not
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    voter_score = models.IntegerField()

    def __str__(self):
        """Return a string representation of this voter"""

        return f'{self.first_name} {self.last_name} ({self.party_affiliation})'

def load_data():
    """Function to load voter records from the CSV file into Django model instance."""

    filename = 'C:/Users/sszha/django/newton_voters.csv'
    f = open(filename, encoding='utf-8')
    f.readline() #discard headers

    #helper to parse dates (year/month/day)
    def parse_date(date_str):
        """convert YYYY-MM-DD string to Python date object, or None if empty"""

        if not date_str.strip():
            return None
        return datetime.strptime(date_str.strip(), '%Y-%m-%d').date()

    def parse_bool(val):
        """Convert a 'TRUE'/'FALSE' string into a Python boolean"""

        return val.strip().upper() == 'TRUE'

    for line in f:
        fields = line.strip().split(',')

        #ensure the row has all the expected columns
        if len(fields) < 17:
            continue

        try:
            voter = Voter(
                voter_id=fields[0],
                first_name=fields[1],
                last_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5],
                zip_code=fields[6],
                date_of_birth=parse_date(fields[7]),
                date_of_registration=parse_date(fields[8]),
                party_affiliation=fields[9].strip(),
                precinct_number=fields[10],
                v20state=parse_bool(fields[11]),
                v21town=parse_bool(fields[12]),
                v21primary=parse_bool(fields[13]),
                v22general=parse_bool(fields[14]),
                v23town=parse_bool(fields[15]),
                voter_score=int(fields[16]) if fields[16] else 0,
            )

            voter.save()

            #print progress every 5000 rows so it doesn't flood terminal
            if Voter.objects.count() % 5000 == 0:
                print(f'Loaded {Voter.objects.count()} voters...')

        except Exception as e:
            print(f"Skipped (Error: {e}): {fields}")

    print(f'Done. Created {len(Voter.objects.all())} Voters.')
