fn main() {
    fn process<A, B>(_a: A, _b: B) {}
    let my_data = process(1, 2);
    let _ = my_data;
}
