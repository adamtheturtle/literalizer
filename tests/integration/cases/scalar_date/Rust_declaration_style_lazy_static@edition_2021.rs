use std::sync::LazyLock;
use chrono::NaiveDate;
#[allow(non_snake_case)]
fn main() {
    #[allow(non_upper_case_globals)]
    static my_data: LazyLock<NaiveDate> = LazyLock::new(|| NaiveDate::from_ymd_opt(2024, 1, 15).unwrap());
    let _ = &my_data;
}
