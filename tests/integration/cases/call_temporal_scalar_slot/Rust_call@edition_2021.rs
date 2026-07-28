use chrono::NaiveDate;
use chrono::NaiveDateTime;
use chrono::NaiveTime;
fn main() {
    fn process<A>(_value: A) {}
    process("09:30:00");
    process(NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), NaiveTime::from_hms_opt(0, 0, 0).unwrap()));
    process(1);
}
