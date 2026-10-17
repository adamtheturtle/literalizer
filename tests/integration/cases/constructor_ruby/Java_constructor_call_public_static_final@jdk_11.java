class Playlist
end

public static final Object p = new Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
