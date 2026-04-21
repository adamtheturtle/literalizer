use std::sync::LazyLock;
use chrono::NaiveDate;
fn main() {
    static my_data: LazyLock<NaiveDate> = LazyLock::new(|| NaiveDate::from_ymd_opt(2024, 1, 15).unwrap());
    let _ = my_data;
}
