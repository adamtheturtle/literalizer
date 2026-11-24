use chrono::NaiveDate;
#[derive(Clone)]
pub struct Record0 {
    pub a: i32,
}
fn main() {
    fn consume<A, B>(_stamp: A, _value: B) {}
    let item = Record0 {
        a: 1,
    };
    let stamp = NaiveDate::from_ymd_opt(2001, 2, 3).unwrap();
    consume(stamp, item.clone());
}
