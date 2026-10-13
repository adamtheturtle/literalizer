use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        HashMap::from([("a", 1)]),
        <HashMap<&str, i32>>::from([]),
    ];
    let _ = &mut my_data;
}
