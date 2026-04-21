fn main() {
    fn process<A>(_value: A) {}
    process("hello");
    process(42);
    process(true);
}
