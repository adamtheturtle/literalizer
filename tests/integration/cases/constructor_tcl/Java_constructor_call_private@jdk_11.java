proc Playlist {} { return 42 }

private Object p = new Playlist();
if {$p != 42} { error "Expected constructor result" }
