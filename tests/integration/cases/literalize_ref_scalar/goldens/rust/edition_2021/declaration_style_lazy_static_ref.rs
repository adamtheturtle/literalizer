use std::sync::LazyLock;
fn main() {
    static MY_INT: LazyLock<i32> = LazyLock::new(|| 42);
    static MY_DATA: LazyLock<i32> = LazyLock::new(|| *MY_INT);
    let _ = &MY_DATA;
}
