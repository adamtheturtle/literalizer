class Playlist
end

let mut p = Playlist::new();
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
