#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    const my_data: [i64; 2] = [
        1,
        1099511627776i64,
    ];
    let _ = &my_data;
}
