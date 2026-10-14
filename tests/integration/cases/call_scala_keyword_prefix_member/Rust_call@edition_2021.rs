fn main() {
    struct PlaylistType;
    impl PlaylistType { fn newValue<A>(&self, _x: A) {} }
    let Playlist = PlaylistType;
    Playlist.newValue(1);
}
