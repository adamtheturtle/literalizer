fn main() {
    fn process<>() {}
    fn emit<A>(__arg: A) {}
    emit(process());
    emit(process());
}
