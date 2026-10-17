proc Playlist {} { return 42 }

static const auto p = Playlist();
if {$p != 42} { error "Expected constructor result" }
