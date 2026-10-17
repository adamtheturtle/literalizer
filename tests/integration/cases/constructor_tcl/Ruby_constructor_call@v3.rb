proc Playlist {} { return 42 }

p = Playlist.new()
if {$p != 42} { error "Expected constructor result" }
