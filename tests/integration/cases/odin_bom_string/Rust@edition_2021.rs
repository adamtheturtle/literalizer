use std::collections::HashMap;
fn main() {
    let my_data = HashMap::from([
        ("v", "a﻿b"),
    ]);
    let _ = my_data;
}
