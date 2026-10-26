fn main() {
    fn process<A>(_data: A) {}
    let unknown_value = ();
    process((unknown_value.clone(),));
}
