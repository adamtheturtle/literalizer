#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        1000000,
        -1234,
        255,
        -10,
    ];
    let _ = &my_data;
    my_data = vec![
        1000000,
        -1234,
        255,
        -10,
    ];
    let _ = &mut my_data;
}
