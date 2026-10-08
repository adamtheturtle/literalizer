fn main() {
    fn process<A>(_value: A) {}
    process(1);  // note<U+2028>still commented<U+2029>done
}
