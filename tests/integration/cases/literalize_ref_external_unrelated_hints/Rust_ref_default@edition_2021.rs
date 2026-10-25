fn assert_equal<Actual, Expected>(actual: Actual, expected: Expected)
where
    Actual: std::fmt::Debug + PartialEq<Expected>,
    Expected: std::fmt::Debug,
{
    assert_eq!(actual, expected);
}
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
    assert_equal(my_data, expected_data);
}
