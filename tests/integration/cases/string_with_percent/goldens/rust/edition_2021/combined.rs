fn main() {
    let mut my_data = vec![
        "100% done",
        "%(name) is here",
    ];
    let _ = &my_data;
    my_data = vec![
        "100% done",
        "%(name) is here",
    ];
    let _ = &mut my_data;
}
