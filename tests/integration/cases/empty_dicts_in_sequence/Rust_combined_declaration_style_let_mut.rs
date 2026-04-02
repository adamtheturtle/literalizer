use std::collections::HashMap;
fn main() {
    {
        let mut my_data = vec![
            HashMap::<String, String>::from([]),
            HashMap::<String, String>::from([]),
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        HashMap::<String, String>::from([]),
        HashMap::<String, String>::from([]),
    ];
    let _ = my_data;
}
