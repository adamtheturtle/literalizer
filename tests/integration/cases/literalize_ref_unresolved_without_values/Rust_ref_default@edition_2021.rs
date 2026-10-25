fn assert_equal<Actual, Expected>(actual: Actual, expected: Expected)
where
    Actual: std::fmt::Debug + PartialEq<Expected>,
    Expected: std::fmt::Debug,
{
    assert_eq!(actual, expected);
}
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
    assert_equal(my_data.clone(), expected_data.clone());
}
