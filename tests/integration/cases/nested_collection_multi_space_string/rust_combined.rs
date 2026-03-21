fn main() {
    {
        let my_data = vec![
            HashMap::from(vec![("key", "hello   world"), ("value", "1")]),
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        HashMap::from(vec![("key", "hello   world"), ("value", "1")]),
    ];
    let _ = my_data;
}
