use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<i32> = LazyLock::new(|| 42);
    let _ = my_data;
}
