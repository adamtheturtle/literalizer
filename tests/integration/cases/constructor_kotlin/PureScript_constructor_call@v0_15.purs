class Playlist { val value = 42 }

data Val
    = PList (Array Val)
p = Playlist
check(p.value == 42)
