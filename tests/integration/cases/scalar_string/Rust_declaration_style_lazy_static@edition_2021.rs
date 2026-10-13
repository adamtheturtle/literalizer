use std::sync::LazyLock;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<&str> = LazyLock::new(|| "hello");
    let _ = &my_data;
}
