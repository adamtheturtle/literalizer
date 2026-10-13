#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        vec![true, false],
        vec![true, true],
    ];
    let _ = &my_data;
    my_data = vec![
        vec![true, false],
        vec![true, true],
    ];
    let _ = &mut my_data;
}
