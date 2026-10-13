#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        "a",  // note a
        "b",  // note b
    ];
    let _ = &my_data;
    my_data = vec![
        "a",  // note a
        "b",  // note b
    ];
    let _ = &mut my_data;
}
