"""Load original exam-bank items. Run from the backend directory:

    python seed_exam_bank.py
"""

from database import SessionLocal
from seeds.exam_bank import seed_exam_bank


def main():
    db = SessionLocal()
    try:
        created = seed_exam_bank(db)
        print(f"inserted {created} new questions")
    finally:
        db.close()


if __name__ == "__main__":
    main()
