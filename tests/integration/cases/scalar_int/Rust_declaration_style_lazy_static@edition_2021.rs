use std::sync::LazyLock;
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<i32> = LazyLock::new(|| 42);
    let _ = &my_data;
}
