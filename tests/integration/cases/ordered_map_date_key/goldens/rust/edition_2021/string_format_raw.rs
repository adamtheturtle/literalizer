use chrono::NaiveDate;
use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        (NaiveDate::from_ymd_opt(2024, 1, 15).unwrap(), r#"value"#),
    ]);
    let _ = &my_data;
}
