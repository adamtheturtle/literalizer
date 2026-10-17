class Playlist
end

static object? p = new Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
