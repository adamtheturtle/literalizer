class Playlist
end

type Val =
    | FList of Val list
let p = Playlist
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
