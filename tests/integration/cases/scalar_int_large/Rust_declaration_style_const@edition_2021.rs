#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    const my_data: i64 = 2147483648i64;
    let _ = &my_data;
}
