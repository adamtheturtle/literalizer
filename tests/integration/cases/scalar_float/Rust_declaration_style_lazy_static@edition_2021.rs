use std::sync::LazyLock;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<f64> = LazyLock::new(|| 3.14);
    let _ = &my_data;
}
