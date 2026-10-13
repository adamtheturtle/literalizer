#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = 3.14;
    let _ = &my_data;
    my_data = 3.14;
    let _ = &mut my_data;
}
