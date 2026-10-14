use std::sync::LazyLock;
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<[i32; 1]> = LazyLock::new(|| [
        1,
    ]);
    let _ = &my_data;
}
