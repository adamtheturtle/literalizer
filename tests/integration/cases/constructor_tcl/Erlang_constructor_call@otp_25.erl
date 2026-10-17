proc Playlist {} { return 42 }

P = 'Playlist'(),
if {$p != 42} { error "Expected constructor result" }
