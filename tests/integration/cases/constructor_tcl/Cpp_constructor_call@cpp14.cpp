proc Playlist {} { return 42 }

auto p = Playlist();
if {$p != 42} { error "Expected constructor result" }
