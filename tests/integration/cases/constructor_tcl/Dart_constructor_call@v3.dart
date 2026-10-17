proc Playlist {} { return 42 }

final p = Playlist();
if {$p != 42} { error "Expected constructor result" }
