class _PlaylistType:
    def newValue(self, *_args: object, **_kwargs: object) -> object: ...
Playlist = _PlaylistType()
Playlist.newValue(x=1)
