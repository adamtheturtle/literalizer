fn main() {
    {
        let my_data = HashMap::from(vec![
            ("date", "2024-01-15"),
            ("datetime", "2024-01-15T12:30:00+00:00"),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from(vec![
        ("date", "2024-01-15"),
        ("datetime", "2024-01-15T12:30:00+00:00"),
    ]);
    let _ = my_data;
}
