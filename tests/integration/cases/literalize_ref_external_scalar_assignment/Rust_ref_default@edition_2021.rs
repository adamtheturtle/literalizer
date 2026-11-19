fn main() {
    let mut my_data = 0;
    let shared = 1;
    assert_eq!(my_data.clone(), 0);
    my_data = shared;
    let expected_data = 1;
    assert_eq!(my_data.clone(), expected_data.clone());
}
