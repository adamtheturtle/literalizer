use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("half", "1979-05-27T07:32:00.500000"),
        ("milli", "1979-05-27T07:32:00.100000"),
        ("max_milli", "1979-05-27T07:32:00.999000"),
        ("whole", "1979-05-27T07:32:00"),
    ]);
    let _ = &my_data;
}
