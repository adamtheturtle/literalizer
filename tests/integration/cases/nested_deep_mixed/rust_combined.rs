use std::collections::HashMap;
use std::collections::HashSet;
fn main() {
    {
        let my_data = vec![
            vec![vec![1, 2], vec!["a", "b"]],
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        vec![vec![1, 2], vec!["a", "b"]],
    ];
    let _ = my_data;
}
