fn main() {
    fn process<A, B>(_value: A, _extra: B) {}
    process(1, "hello");
    process("two", false);
    process(3.5, None::<()>);
}
