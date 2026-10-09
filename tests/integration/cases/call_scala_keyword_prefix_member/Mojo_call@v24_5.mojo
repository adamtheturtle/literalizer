@fieldwise_init
struct _PlaylistType(Copyable, Movable):
    def newValue(self, x: Int):
        pass
def main():
    var Playlist = _PlaylistType()
    Playlist.newValue(1)
