use std::collections::HashMap;
fn main() {
    {
        let mut my_data = HashMap::from([
            ("key", "\"bang!\""),  // real
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from([
        ("key", "\"bang!\""),  // real
    ]);
    let _ = my_data;
}
