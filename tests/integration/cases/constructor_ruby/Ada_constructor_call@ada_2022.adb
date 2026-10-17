class Playlist
end

p : A_Val := Playlist;
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
