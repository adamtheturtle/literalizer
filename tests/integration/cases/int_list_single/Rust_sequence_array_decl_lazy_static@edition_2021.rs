use std::sync::LazyLock;
fn main() {
    static my_data: LazyLock<[i32; 1]> = LazyLock::new(|| [
        1,
    ]);
    let _ = my_data;
}
