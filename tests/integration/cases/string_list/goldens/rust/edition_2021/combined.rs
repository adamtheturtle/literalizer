fn main() {
    let mut my_data = vec![
        "foo",
        "bar",
        "baz",
    ];
    let _ = &my_data;
    my_data = vec![
        "foo",
        "bar",
        "baz",
    ];
    let _ = &mut my_data;
}
