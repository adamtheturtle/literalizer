#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: (i32, i32, i32) = (
        1,
        2,
        3,
    );
    let _ = &my_data;
}
