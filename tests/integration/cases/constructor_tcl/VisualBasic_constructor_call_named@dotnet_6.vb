proc Playlist {} { return 42 }

Dim p = New Playlist()
if {$p != 42} { error "Expected constructor result" }
