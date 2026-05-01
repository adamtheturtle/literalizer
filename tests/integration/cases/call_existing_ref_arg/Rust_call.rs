fn main() {
    fn send<A>(_value: A) {}
    let existing = 42;
    send(existing);
}
