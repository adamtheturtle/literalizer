fn main() {
    fn record_value<A>(_value: A) {}
    fn flush_buffer<A>(_count: A) {}
    fn emit<A>(__arg: A) {}
    emit(record_value(42));
    flush_buffer(3);
}
