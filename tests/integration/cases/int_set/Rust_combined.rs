use std::collections::HashSet;
fn main() {
    {
        let my_data = HashSet::from([
            1,
            2,
            3,
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashSet::from([
        1,
        2,
        3,
    ]);
    let _ = my_data;
}
