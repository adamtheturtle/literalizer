module ConstructorBinding
class Playlist
end

type(fval_t) :: p
p = Playlist()
raise "Expected a Playlist instance" unless p.is_a?(Playlist)
end
