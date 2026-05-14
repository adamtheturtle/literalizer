use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<Vec<&str>> = LazyLock::new(|| vec![
        "48656c6c6f",
    ]);
    let _ = my_data;
}
