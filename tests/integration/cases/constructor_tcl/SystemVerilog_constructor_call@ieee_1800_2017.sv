proc Playlist {} { return 42 }

static _VVal p = Playlist();
if {$p != 42} { error "Expected constructor result" }
