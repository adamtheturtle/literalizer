use std::sync::LazyLock;
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<i64> = LazyLock::new(|| 2147483648i64);
    let _ = &my_data;
}
