class Playlist
end

const p = Playlist();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
