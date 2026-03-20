struct V;
impl From<i32> for V { fn from(_: i32) -> Self { V } }
impl From<i64> for V { fn from(_: i64) -> Self { V } }
impl From<f64> for V { fn from(_: f64) -> Self { V } }
impl From<bool> for V { fn from(_: bool) -> Self { V } }
impl From<&str> for V { fn from(_: &str) -> Self { V } }
impl<T> From<Option<T>> for V { fn from(_: Option<T>) -> Self { V } }
impl<T> From<std::vec::Vec<T>> for V { fn from(_: std::vec::Vec<T>) -> Self { V } }
impl<A, B> From<(A, B)> for V { fn from(_: (A, B)) -> Self { V } }
macro_rules! vec {
    () => { ::std::vec::Vec::<V>::new() };
    ($($e:expr),+ $(,)?) => {{
        let mut _v = ::std::vec::Vec::<V>::new();
        $(_v.push(<V as From<_>>::from($e));)+
        _v
    }};
}
fn main() {
    let _ = vec![
        vec![1, "a"],
        vec![2, "b"],
    ];
}
