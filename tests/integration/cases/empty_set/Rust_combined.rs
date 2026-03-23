use std::collections::HashSet;
fn main() {
    {
        let my_data = HashSet::<String>::new();
        let _ = my_data;
    }
    let my_data;
    my_data = HashSet::<String>::new();
    let _ = my_data;
}
