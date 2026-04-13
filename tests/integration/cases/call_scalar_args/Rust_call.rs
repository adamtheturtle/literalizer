fn main() {
    fn process(_value: &dyn std::any::Any) {}
    process("hello");
    process(42);
    process(true);
    let _ = my_data;
}
