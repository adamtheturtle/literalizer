use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    {
        let my_data = vec![
            HashSet::from([]),
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        HashSet::from([]),
    ];
    let _ = my_data;
}
