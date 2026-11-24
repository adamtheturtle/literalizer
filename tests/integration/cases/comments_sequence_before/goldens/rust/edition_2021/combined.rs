fn main() {
    let mut my_data = vec![
        // first
        "a",
        // second
        "b",
    ];
    let _ = &my_data;
    my_data = vec![
        // first
        "a",
        // second
        "b",
    ];
    let _ = &mut my_data;
}
