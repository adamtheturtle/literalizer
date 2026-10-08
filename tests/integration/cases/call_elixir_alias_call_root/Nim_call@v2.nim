type PlaylistType = object
template new(self: PlaylistType; args: varargs[untyped]) = discard
var Playlist: PlaylistType
Playlist.new(1)
Playlist.new(2)
