proc Playlist {} { return 42 }

def p = new Playlist()
if {$p != 42} { error "Expected constructor result" }
