class Playlist
end

type val_t =
  | OList of val_t list
let p = Playlist()
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
