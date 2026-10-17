struct Playlist { let value = 42 }

data Val = HList [Val]
p = Playlist()
precondition(p.value == 42)
