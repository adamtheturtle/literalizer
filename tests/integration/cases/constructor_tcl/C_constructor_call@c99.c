proc Playlist {} { return 42 }

CVal p = Playlist();
if {$p != 42} { error "Expected constructor result" }
