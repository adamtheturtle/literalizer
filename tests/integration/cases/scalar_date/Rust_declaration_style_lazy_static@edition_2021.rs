use std::sync::LazyLock;
use chrono::NaiveDate;
fn main() {
    static MY_DATA: LazyLock<NaiveDate> = LazyLock::new(|| NaiveDate::from_ymd_opt(2024, 1, 15).unwrap());
    let _ = &MY_DATA;
}
