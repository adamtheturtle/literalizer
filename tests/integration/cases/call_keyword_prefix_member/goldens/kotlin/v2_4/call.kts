class _PlaylistType { fun newValue(x: Any? = null): Any? = listOf<Any?>(x) }
val Playlist = _PlaylistType()
Playlist.newValue(x = 1)
