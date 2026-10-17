proc Playlist {} { return 42 }

data Val
    = PList (Array Val)
p = Playlist
if {$p != 42} { error "Expected constructor result" }
