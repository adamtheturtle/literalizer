fn main() {
    {
        let my_data = HashMap::from(vec![
            ("key\nwith\nnewlines", "value1"),
            ("key\twith\ttabs", "value2"),
            ("", "value3"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from(vec![
        ("key\nwith\nnewlines", "value1"),
        ("key\twith\ttabs", "value2"),
        ("", "value3"),
    ]);
    let _ = my_data;
}
