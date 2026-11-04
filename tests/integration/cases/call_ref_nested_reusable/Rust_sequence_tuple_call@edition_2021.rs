fn main() {
    fn process<A>(_data: A) {}
    let item = (
        1,
        2,
    );
    process((item, item));
}
