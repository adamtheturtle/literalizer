#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        0.0,
        1.0,
        1500.0,
        0.001,
        1.0e+16,
    ];
    let _ = &my_data;
    my_data = vec![
        0.0,
        1.0,
        1500.0,
        0.001,
        1.0e+16,
    ];
    let _ = &mut my_data;
}
