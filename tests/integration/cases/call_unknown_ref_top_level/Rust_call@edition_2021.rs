#[allow(non_snake_case)]
fn main() {
    fn process<A>(_data: A) {}
    let unknown_value = vec![
        1,
    ];
    process(unknown_value);
}
