use std::sync::LazyLock;
fn main() {
    static MY_DATA: LazyLock<Vec<String>> = LazyLock::new(|| Vec::<String>::new());
    let _ = &MY_DATA;
}
