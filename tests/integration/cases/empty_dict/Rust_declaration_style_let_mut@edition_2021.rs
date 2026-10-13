use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::<String, String>::from([]);
    let _ = &mut my_data;
}
