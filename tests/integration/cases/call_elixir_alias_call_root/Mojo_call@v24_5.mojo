@fieldwise_init
struct _PlaylistType(Copyable, Movable):
    def new(self, x: Int):
        pass
def main():
    var Playlist = _PlaylistType()
    Playlist.new(1)
    Playlist.new(2)
