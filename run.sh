if [[ -f *.pyc ]]; then rm *.pyc; fi
if [[ -f fta.sqlite ]]; then rm fta.sqlite; fi

python run_scraper.py
