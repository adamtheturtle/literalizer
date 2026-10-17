proc Playlist {} { return 42 }

p : A_Val := Playlist;
if {$p != 42} { error "Expected constructor result" }
