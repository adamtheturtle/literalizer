proc Playlist {} { return 42 }

static Object p = new Playlist();
if {$p != 42} { error "Expected constructor result" }
