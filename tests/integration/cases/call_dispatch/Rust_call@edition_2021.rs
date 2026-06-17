fn main() {
    fn store_item<A, B>(_key: A, _value: B) {}
    fn read_item<A>(_key: A) {}
    store_item(1, 10);
    read_item(1);
}
