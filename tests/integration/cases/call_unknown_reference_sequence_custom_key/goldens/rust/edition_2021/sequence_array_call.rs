fn main() {
    fn process<A>(_data: A) {}
    let untyped_value = [] as [String; 0];
    process([untyped_value.clone(), untyped_value.clone()]);
}
