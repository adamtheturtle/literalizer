fn main() {
    let missing = vec![
        1,
        2,
    ];
    let my_data = missing;
    let expected_data = vec![
        1,
        2,
    ];
    assert_eq!(my_data.clone(), expected_data.clone());
}
