if [[ -f *.pyc ]]; then rm *.pyc; fi
if [[ -f fta.sqlite ]]; then rm fta.sqlite; fi
sqlite3 fta.sqlite "CREATE TABLE IF NOT EXISTS queries (query TEXT, date DATE)"

python run_scraper.py
