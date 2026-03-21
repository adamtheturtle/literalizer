fn main() {
    {
        let my_data = HashMap::from(vec![
            ("name", "Alice"),
            ("age", "30"),
            ("active", "True"),
            ("score", "None"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from(vec![
        ("name", "Alice"),
        ("age", "30"),
        ("active", "True"),
        ("score", "None"),
    ]);
    let _ = my_data;
}
