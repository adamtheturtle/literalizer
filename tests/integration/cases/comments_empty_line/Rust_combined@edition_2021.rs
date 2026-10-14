fn main() {
    let mut my_data = vec![
        "a",
        //
        "b",
    ];
    let _ = &my_data;
    my_data = vec![
        "a",
        //
        "b",
    ];
    let _ = &mut my_data;
}
