fn main() {
    struct PlaylistType_;
    impl PlaylistType_ { fn new<A>(&self, _x: A) {} }
    let Playlist = PlaylistType_;
    Playlist.new(1);
}
