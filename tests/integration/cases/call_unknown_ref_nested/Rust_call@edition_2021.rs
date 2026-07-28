fn main() {
    fn process<A, B>(_known_value: A, _nested_missing: B) {}
    let known_value = true;
    let unknown_value = true;
    process(known_value, unknown_value);
}
