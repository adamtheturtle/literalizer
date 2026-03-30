fn main() {
    {
        let my_data = vec![
            "C:\\path\\to\\file",
            "back\\\\slash",
            "hello \\\"world\\\"",
            "path\\to \"# file",
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        "C:\\path\\to\\file",
        "back\\\\slash",
        "hello \\\"world\\\"",
        "path\\to \"# file",
    ];
    let _ = my_data;
}
