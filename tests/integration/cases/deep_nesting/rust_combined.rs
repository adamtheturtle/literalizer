fn main() {
    {
        let my_data = HashMap::from(vec![
            ("level1", HashMap::from(vec![("level2", "{\"level3\": \"{\\\"level4\\\": {\\\"value\\\": \\\"deep\\\", \\\"items\\\": \\\"[\\\\\\\"a\\\\\\\", \\\\\\\"b\\\\\\\"]\\\"}}\", \"sibling\": \"42\"}"), ("tags", "[{\"name\": \"tag1\", \"meta\": \"{\\\"priority\\\": \\\"1\\\", \\\"labels\\\": \\\"[\\\\\\\"x\\\\\\\", \\\\\\\"y\\\\\\\"]\\\"}\"}]")])),
        ]);
        let _ = my_data;
    }
    let my_data;
    my_data = HashMap::from(vec![
        ("level1", HashMap::from(vec![("level2", "{\"level3\": \"{\\\"level4\\\": {\\\"value\\\": \\\"deep\\\", \\\"items\\\": \\\"[\\\\\\\"a\\\\\\\", \\\\\\\"b\\\\\\\"]\\\"}}\", \"sibling\": \"42\"}"), ("tags", "[{\"name\": \"tag1\", \"meta\": \"{\\\"priority\\\": \\\"1\\\", \\\"labels\\\": \\\"[\\\\\\\"x\\\\\\\", \\\\\\\"y\\\\\\\"]\\\"}\"}]")])),
    ]);
    let _ = my_data;
}
