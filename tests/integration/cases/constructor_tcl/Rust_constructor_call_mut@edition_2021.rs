proc Playlist {} { return 42 }

let mut p = Playlist::new();
if {$p != 42} { error "Expected constructor result" }
