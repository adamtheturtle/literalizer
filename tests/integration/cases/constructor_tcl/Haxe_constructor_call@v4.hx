proc Playlist {} { return 42 }

final p = new Playlist();
if {$p != 42} { error "Expected constructor result" }
