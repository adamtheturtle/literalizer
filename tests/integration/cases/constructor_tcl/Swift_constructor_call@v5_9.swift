proc Playlist {} { return 42 }

let p = Playlist()
if {$p != 42} { error "Expected constructor result" }
