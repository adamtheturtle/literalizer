use std::sync::LazyLock;
fn main() {
    static MY_DATA: LazyLock<Vec<&str>> = LazyLock::new(|| vec![
        "48656c6c6f",
    ]);
    let _ = &MY_DATA;
}
