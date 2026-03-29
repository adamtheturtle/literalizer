use std::collections::HashMap;
fn main() {
    {
        let my_data = HashMap::<String, String>::from([]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::<String, String>::from([]);
    let _ = my_data;
}
