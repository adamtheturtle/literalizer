proc Playlist {} { return 42 }

set p [Playlist]
if {$p != 42} { error "Expected constructor result" }
