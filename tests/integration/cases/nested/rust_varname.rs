fn main() {
    let my_data = HashMap::from(vec![
        ("users", vec![HashMap::from(vec![("name", "Bob"), ("tags", "[\"admin\", \"user\"]")]), HashMap::from(vec![("name", "Carol"), ("tags", "[\"guest\"]")])]),
    ]);
    let _ = my_data;
}
