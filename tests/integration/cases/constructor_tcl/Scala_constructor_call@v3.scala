proc Playlist {} { return 42 }

val p = new Playlist()
if {$p != 42} { error "Expected constructor result" }
