use std::collections::{HashMap};
fn main() {
    let _ = HashMap::from([
        ("level1", HashMap::from([("level2", "{\"level3\": \"{\\\"level4\\\": {\\\"value\\\": \\\"deep\\\", \\\"items\\\": \\\"[\\\\\\\"a\\\\\\\", \\\\\\\"b\\\\\\\"]\\\"}}\", \"sibling\": \"42\"}"), ("tags", "[{\"name\": \"tag1\", \"meta\": \"{\\\"priority\\\": \\\"1\\\", \\\"labels\\\": \\\"[\\\\\\\"x\\\\\\\", \\\\\\\"y\\\\\\\"]\\\"}\"}]")])),
    ]);
}
