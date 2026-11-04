fn main() {
    fn process<A>(_data: A) {}
    let item = vec![
        1,
        2,
    ];
    process(vec![item.clone(), item.clone()]);
}
