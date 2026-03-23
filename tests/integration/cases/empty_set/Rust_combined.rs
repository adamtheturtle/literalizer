use std::collections::HashSet;
fn main() {
    {
        let my_data = vec![
            HashSet::<String>::from([]),
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        HashSet::<String>::from([]),
    ];
    let _ = my_data;
}
