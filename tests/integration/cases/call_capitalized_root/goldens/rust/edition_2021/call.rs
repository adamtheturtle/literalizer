// Preserve intentional caller identifier spelling.
#![allow(non_snake_case)]
fn main() {
    struct PlaylistType;
    impl PlaylistType { fn new<A>(&self, _x: A) {} }
    let Playlist = PlaylistType;
    Playlist.new(1);
    Playlist.new(2);
}
