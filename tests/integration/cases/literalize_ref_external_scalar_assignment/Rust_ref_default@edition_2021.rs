fn assert_equal<Actual, Expected>(actual: Actual, expected: Expected)
where
    Actual: std::fmt::Debug + PartialEq<Expected>,
    Expected: std::fmt::Debug,
{
    assert_eq!(actual, expected);
}
fn main() {
    let mut my_data = 0;
    let shared = 1;
    assert_equal(my_data.clone(), 0);
    my_data = shared;
    let expected_data = 1;
    assert_equal(my_data.clone(), expected_data.clone());
}
