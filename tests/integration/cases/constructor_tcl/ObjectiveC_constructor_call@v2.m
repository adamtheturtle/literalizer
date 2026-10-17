proc Playlist {} { return 42 }

id p = Playlist();
if {$p != 42} { error "Expected constructor result" }
