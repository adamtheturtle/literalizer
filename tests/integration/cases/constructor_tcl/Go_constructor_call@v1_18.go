proc Playlist {} { return 42 }

p := NewPlaylist()
if {$p != 42} { error "Expected constructor result" }
