fn main() {
    struct PlaylistType_;
    impl PlaylistType_ { fn newValue<A>(&self, _x: A) {} }
    let Playlist = PlaylistType_;
    Playlist.newValue(1);
}
