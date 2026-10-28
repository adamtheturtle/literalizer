fn main() {
    fn process<A>(_value: A) {}
    process(None::<()>);
    process(vec![1, 2]);
}
