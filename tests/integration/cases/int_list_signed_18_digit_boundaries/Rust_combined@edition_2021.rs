#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        999999999999999999i64,
        -999999999999999999i64,
    ];
    let _ = &my_data;
    my_data = vec![
        999999999999999999i64,
        -999999999999999999i64,
    ];
    let _ = &mut my_data;
}
