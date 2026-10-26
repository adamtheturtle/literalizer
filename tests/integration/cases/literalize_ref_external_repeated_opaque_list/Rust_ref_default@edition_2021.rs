fn assert_equal<Actual, Expected>(actual: Actual, expected: Expected)
where
    Actual: std::fmt::Debug + PartialEq<Expected>,
    Expected: std::fmt::Debug,
{
    assert_eq!(actual, expected);
}
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
    assert_equal(my_data.clone(), expected_data.clone());
}
