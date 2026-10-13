#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        f64::INFINITY,
        f64::NEG_INFINITY,
        f64::NAN,
    ];
    let _ = &my_data;
    my_data = vec![
        f64::INFINITY,
        f64::NEG_INFINITY,
        f64::NAN,
    ];
    let _ = &mut my_data;
}
