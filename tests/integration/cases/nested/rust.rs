fn main() {
    let _ = HashMap::from(vec![
        ("users", vec![HashMap::from(vec![("name", "Bob"), ("tags", "[\"admin\", \"user\"]")]), HashMap::from(vec![("name", "Carol"), ("tags", "[\"guest\"]")])]),
    ]);
}
