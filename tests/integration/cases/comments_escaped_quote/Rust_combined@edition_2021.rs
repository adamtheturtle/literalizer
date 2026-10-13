use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::from([
        ("key", "value \" # not a comment"),  // real
    ]);
    let _ = &my_data;
    my_data = HashMap::from([
        ("key", "value \" # not a comment"),  // real
    ]);
    let _ = &mut my_data;
}
