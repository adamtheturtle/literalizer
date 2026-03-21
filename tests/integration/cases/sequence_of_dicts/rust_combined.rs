fn main() {
    {
        let my_data = vec![
            HashMap::from(vec![("name", "Alice"), ("age", "30")]),
            HashMap::from(vec![("name", "Bob"), ("age", "25")]),
        ];
        let _ = my_data;
    }
    let my_data;
    my_data = vec![
        HashMap::from(vec![("name", "Alice"), ("age", "30")]),
        HashMap::from(vec![("name", "Bob"), ("age", "25")]),
    ];
    let _ = my_data;
}
