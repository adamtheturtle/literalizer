// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
fn main() {
    struct PlaylistType;
    impl PlaylistType { fn newValue<A>(&self, _x: A) {} }
    let Playlist = PlaylistType;
    Playlist.newValue(1);
}
