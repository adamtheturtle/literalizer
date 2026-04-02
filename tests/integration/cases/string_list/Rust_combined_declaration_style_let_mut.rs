fn main() {
    {
        let mut my_data = vec![
            "foo",
            "bar",
            "baz",
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        "foo",
        "bar",
        "baz",
    ];
    let _ = my_data;
}
