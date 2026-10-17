struct Playlist { let value = 42 }

(def p (Playlist))
precondition(p.value == 42)
