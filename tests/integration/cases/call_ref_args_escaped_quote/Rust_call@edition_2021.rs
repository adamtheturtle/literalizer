#[allow(non_snake_case)]
fn main() {
    fn process<A>(_v: A) {}
    let my_str = "a\"b";
    process(my_str);
}
