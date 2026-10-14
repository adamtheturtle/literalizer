fn main() {
    struct PlaylistType;
    impl PlaylistType { fn new<A>(&self, _x: A) {} }
    let Playlist = PlaylistType;
    Playlist.new(1);
}
