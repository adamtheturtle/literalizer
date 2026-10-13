#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: f64 = 3.14;
    let _ = &my_data;
}
