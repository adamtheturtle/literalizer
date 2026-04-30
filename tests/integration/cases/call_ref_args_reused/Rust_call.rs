fn main() {
    fn process<A, B>(_data: A, _count: B) {}
    let shared = 1;
    let other = 2;
    process(shared, 1);
    process(other, 0);
    process(shared, 8);
}
