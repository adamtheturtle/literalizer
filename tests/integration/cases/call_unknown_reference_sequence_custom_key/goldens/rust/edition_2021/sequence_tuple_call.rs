fn main() {
    fn process<A>(_data: A) {}
    let untyped_value = ();
    process((untyped_value.clone(), untyped_value.clone()));
}
