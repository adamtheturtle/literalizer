fn main() {
    struct Playlist;
    impl Playlist { fn new() -> Self { Self } }
    let mut created = Playlist::new();
    let _ = &mut created;
}
