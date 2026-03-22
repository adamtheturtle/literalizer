fn main() {
    {
        let my_data = vec![
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
