proc Playlist {} { return 42 }

local p = Playlist()
if {$p != 42} { error "Expected constructor result" }
