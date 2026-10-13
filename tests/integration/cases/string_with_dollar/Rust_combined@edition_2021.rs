#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        "price $10",
        "$HOME",
    ];
    let _ = &my_data;
    my_data = vec![
        "price $10",
        "$HOME",
    ];
    let _ = &mut my_data;
}
