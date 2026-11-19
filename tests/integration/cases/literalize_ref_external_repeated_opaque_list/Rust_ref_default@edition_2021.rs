fn main() {
    let item = Vec::<String>::new();
    let my_data = vec![
        item.clone(),
        item.clone(),
    ];
    let expected_data = vec![
        Vec::<String>::new(),
        Vec::<String>::new(),
    ];
    assert_eq!(my_data.clone(), expected_data.clone());
}
