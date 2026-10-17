proc Playlist {} { return 42 }

var p = Playlist.new()
if {$p != 42} { error "Expected constructor result" }
