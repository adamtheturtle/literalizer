#[allow(non_snake_case)]
fn main() {
    fn process<A>(_value: A) {}
    process("Dune");  // first edition
    process("Solaris");
    process("Neuromancer");  // cyberpunk
}
