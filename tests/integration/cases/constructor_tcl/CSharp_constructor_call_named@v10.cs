proc Playlist {} { return 42 }

var p = new Playlist();
if {$p != 42} { error "Expected constructor result" }
