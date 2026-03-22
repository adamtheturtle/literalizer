fn main() {
    {
        let my_data = vec![
            "42",
            "3.14",
            "True",
            "False",
            "hello \"world\"",
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        "42",
        "3.14",
        "True",
        "False",
        "hello \"world\"",
    ];
    let _ = my_data;
}
