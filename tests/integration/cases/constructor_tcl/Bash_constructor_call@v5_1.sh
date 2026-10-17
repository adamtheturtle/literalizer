proc Playlist {} { return 42 }

declare p="$(Playlist)"
if {$p != 42} { error "Expected constructor result" }
