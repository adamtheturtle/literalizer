use std::sync::LazyLock;
fn main() {
    static MY_DATA: LazyLock<i32> = LazyLock::new(|| 42);
    let _ = &MY_DATA;
}
