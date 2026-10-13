#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = "hello # world";
    let _ = &my_data;
    my_data = "hello # world";
    let _ = &mut my_data;
}
