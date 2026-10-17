proc Playlist {} { return 42 }

const p = new Playlist({  });
if {$p != 42} { error "Expected constructor result" }
