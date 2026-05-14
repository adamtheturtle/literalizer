use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<Vec<String>> = LazyLock::new(|| Vec::<String>::new());
    let _ = my_data;
}
