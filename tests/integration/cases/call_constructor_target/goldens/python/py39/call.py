class _PlaylistType:
    def new(self, *_args: object, **_kwargs: object) -> object: ...
Playlist = _PlaylistType()
Playlist.new(x=1)
