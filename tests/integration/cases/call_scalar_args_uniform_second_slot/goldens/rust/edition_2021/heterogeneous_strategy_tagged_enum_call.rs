fn main() {
    fn process<A, B>(_value: A, _label: B) {}
    process("hello", "a");
    process(42, "b");
    process(true, "c");
}
