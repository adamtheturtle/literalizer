fn main() {
    let a = 0;
    let my_data = vec![
        a,
        1,
    ];
    let expected_data = vec![
        0,
        1,
    ];
    assert_eq!(my_data.clone(), expected_data.clone());
}
