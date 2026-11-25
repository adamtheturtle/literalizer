fn main() {
    let mut my_data = vec![
        // # section
        "a",
    ];
    let _ = &my_data;
    my_data = vec![
        // # section
        "a",
    ];
    let _ = &mut my_data;
}
