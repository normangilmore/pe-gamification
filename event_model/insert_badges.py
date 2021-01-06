from sqlalchemy import create_engine
from event_model.badge import Badge
from sqlalchemy.orm import sessionmaker
import csv

engine = create_engine("postgresql://pe_dashboard:test-only-yVu8W5azUtZ8RPSWX42o@localhost:5432/pe_dashboard", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def insert_badges(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Run query on badge table, if empty, then add new badge (result == None)
            in_badge = session.query(Badge).filter(Badge.name == row['name']).first()
            if in_badge is None:
                b = Badge(id=row['badge_id'], name=row['name'])
                session.add(b)
                session.commit()

if __name__ == "__main__":
    insert_badges('badge_list.csv')