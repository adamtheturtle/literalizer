use std::collections::HashMap;
fn main() {
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
