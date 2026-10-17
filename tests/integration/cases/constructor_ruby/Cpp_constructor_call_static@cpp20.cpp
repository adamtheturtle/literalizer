class Playlist
end

static auto p = Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
