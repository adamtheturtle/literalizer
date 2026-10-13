#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        Vec::<String>::new(),
        Vec::<String>::new(),
    ];
    let _ = &my_data;
    my_data = vec![
        Vec::<String>::new(),
        Vec::<String>::new(),
    ];
    let _ = &mut my_data;
}
