fn main() {
    {
        let mut my_data = vec![
            "line1\r\nline2",
            "line1\rline2",
            "",
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        "line1\r\nline2",
        "line1\rline2",
        "",
    ];
    let _ = my_data;
}
