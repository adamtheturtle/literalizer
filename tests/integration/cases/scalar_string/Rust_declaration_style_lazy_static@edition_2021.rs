use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<&str> = LazyLock::new(|| "hello");
    let _ = my_data;
}
