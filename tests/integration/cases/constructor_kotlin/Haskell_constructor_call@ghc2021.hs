class Playlist { val value = 42 }

data Val = HList [Val]
p = Playlist
check(p.value == 42)
