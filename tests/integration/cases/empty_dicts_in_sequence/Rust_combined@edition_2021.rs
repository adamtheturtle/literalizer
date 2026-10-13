use std::collections::HashMap;
#[allow(non_snake_case)]
fn main() {
    #[allow(unused_mut)]
    let mut my_data = vec![
        HashMap::<String, String>::from([]),
        HashMap::<String, String>::from([]),
    ];
    let _ = &my_data;
    my_data = vec![
        HashMap::<String, String>::from([]),
        HashMap::<String, String>::from([]),
    ];
    let _ = &mut my_data;
}
