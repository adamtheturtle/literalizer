#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = 9223372036854775808i128;
    let _ = &my_data;
    my_data = 9223372036854775808i128;
    let _ = &mut my_data;
}
