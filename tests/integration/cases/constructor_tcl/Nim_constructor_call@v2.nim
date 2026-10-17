proc Playlist {} { return 42 }

var p = Playlist()
if {$p != 42} { error "Expected constructor result" }
