use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    {
        let my_data = vec![
            vec![true, false],
            vec![true, true],
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        vec![true, false],
        vec![true, true],
    ];
    let _ = my_data;
}
