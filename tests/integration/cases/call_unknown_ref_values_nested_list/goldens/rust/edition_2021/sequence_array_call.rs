fn main() {
    fn process<A>(_data: A) {}
    let unknown_value = [] as [String; 0];
    process([unknown_value.clone()]);
}
