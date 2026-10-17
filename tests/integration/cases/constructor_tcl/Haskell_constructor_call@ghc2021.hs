proc Playlist {} { return 42 }

data Val = HList [Val]
p = Playlist
if {$p != 42} { error "Expected constructor result" }
