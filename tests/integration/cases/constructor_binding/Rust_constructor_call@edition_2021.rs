fn main() {
    struct Playlist;
    impl Playlist { fn new() -> Self { Self } }
    let created = Playlist::new();
    let _ = &created;
}
