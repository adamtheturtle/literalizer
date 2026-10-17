class Playlist
end

static _VVal p = Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
