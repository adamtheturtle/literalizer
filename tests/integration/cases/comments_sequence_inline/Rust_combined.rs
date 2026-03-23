fn main() {
    {
        let my_data = vec![
            "a",  // note a
            "b",  // note b
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        "a",  // note a
        "b",  // note b
    ];
    let _ = my_data;
}
