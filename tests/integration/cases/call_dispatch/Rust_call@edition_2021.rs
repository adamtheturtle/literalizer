fn main() {
    fn put<A, B>(_key: A, _value: B) {}
    fn get<A>(_key: A) {}
    put(1, 10);
    get(1);
}
