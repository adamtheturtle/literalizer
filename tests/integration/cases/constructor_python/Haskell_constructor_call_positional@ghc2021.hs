class Playlist:
    pass


data Val = HList [Val]
p = Playlist()
assert isinstance(p, Playlist)
