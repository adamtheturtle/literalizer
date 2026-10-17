module ConstructorBinding
class Playlist
end

datatype val_t =
    SList of val_t list
val p = Playlist()
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end
