fn assert_equal<Actual, Expected>(actual: Actual, expected: Expected)
where
    Actual: std::fmt::Debug + PartialEq<Expected>,
    Expected: std::fmt::Debug,
{
    assert_eq!(actual, expected);
}
