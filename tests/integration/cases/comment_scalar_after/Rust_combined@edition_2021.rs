#[allow(non_snake_case)]
fn main() {
    // after
    #[allow(unused_mut)]
    let mut my_data = 42;
    let _ = &my_data;
    // after
    my_data = 42;
    let _ = &mut my_data;
}
