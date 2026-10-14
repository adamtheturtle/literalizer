fn main() {
    fn process<A>(_value: A) {}
    // Test cases
    process("hello");  // single word
    process("hello world");  // two words
    // trailing comment
}
