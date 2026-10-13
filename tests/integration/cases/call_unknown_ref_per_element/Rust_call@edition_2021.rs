#[allow(non_snake_case)]
fn main() {
    fn process<A>(_data: A) {}
    let unknown_value = Vec::<String>::new();
    process(unknown_value);
}
