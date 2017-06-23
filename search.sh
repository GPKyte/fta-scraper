query="$*"

sqlite3 fta.sqlite -separator " | " "SELECT link, description FROM items WHERE description LIKE '%$query%'"
sqlite3 fta.sqlite "INSERT INTO queries VALUES ('$query', '$(date)')"
