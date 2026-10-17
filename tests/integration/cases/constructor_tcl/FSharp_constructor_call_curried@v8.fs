proc Playlist {} { return 42 }

type Val =
    | FList of Val list
let p = Playlist
if {$p != 42} { error "Expected constructor result" }
