use std::sync::LazyLock;
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<&str> = LazyLock::new(|| "hello");
    let _ = &my_data;
}
