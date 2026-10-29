type PlaylistType = object
template newValue(self: PlaylistType; args: varargs[untyped]) = discard
var Playlist: PlaylistType
Playlist.newValue(1)
