fn main() {
    fn process<A>(_data: A) {}
    let known_value = 1;
    let unknown_value = Vec::<String>::new();
    process(unknown_value);
}
