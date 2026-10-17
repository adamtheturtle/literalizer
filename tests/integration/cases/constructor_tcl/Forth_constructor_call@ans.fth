proc Playlist {} { return 42 }

: p Playlist ;
if {$p != 42} { error "Expected constructor result" }
