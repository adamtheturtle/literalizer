fn main() {
    fn process<A>(_data: A) {}
    let untyped_value = Vec::<String>::new();
    process(vec![untyped_value.clone(), untyped_value.clone()]);
}
