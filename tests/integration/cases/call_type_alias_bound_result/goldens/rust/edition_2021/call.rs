fn main() {
    fn process<A>(_value: A) {}
    let my_data = process(1);
    let _ = &my_data;
}
