#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: i32 = 42;
    let _ = &my_data;
}
