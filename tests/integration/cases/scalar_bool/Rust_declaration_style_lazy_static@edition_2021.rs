use std::sync::LazyLock;
fn main() {
    static MY_DATA: LazyLock<bool> = LazyLock::new(|| true);
    let _ = &MY_DATA;
}
