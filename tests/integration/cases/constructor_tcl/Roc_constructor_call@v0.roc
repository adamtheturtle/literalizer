proc Playlist {} { return 42 }

Val : [
    RList (List Val),
]
p = Playlist
if {$p != 42} { error "Expected constructor result" }
