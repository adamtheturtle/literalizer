use std::collections::HashMap;
fn main() {
    {
        let my_data = vec![
            HashMap::<&str, &str>::from([]),
            HashMap::<&str, &str>::from([]),
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        HashMap::<&str, &str>::from([]),
        HashMap::<&str, &str>::from([]),
    ];
    let _ = my_data;
}
