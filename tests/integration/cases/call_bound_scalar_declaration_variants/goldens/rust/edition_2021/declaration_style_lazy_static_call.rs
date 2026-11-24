use std::sync::LazyLock;
fn main() {
    fn consume<A>(_value: A) {}
    static SHARED: LazyLock<i32> = LazyLock::new(|| 42);
    consume(*SHARED);
}
