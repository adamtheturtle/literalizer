use std::sync::LazyLock;
fn main() {
    static MY_DATA: LazyLock<&str> = LazyLock::new(|| "hello");
    let _ = &MY_DATA;
}
