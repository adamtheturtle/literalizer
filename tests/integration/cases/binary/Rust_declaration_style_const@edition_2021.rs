#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    const my_data: [&str; 1] = [
        "48656c6c6f",
    ];
    let _ = &my_data;
}
