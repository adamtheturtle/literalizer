proc Playlist {} { return 42 }

public static final Object p = new Playlist();
if {$p != 42} { error "Expected constructor result" }
