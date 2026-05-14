use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<[i32; 3]> = LazyLock::new(|| [
        1,
        2,
        3,
    ]);
    let _ = my_data;
}
