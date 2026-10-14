use std::collections::HashMap;
fn main() {
    #[allow(unused_mut)]
    let mut my_data = HashMap::<String, String>::from([]);
    let _ = &my_data;
    my_data = HashMap::<String, String>::from([]);
    let _ = &mut my_data;
}
