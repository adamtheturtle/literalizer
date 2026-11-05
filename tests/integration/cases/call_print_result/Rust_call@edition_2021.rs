fn main() {
    fn calculate<A>(_value: A) {}
    println!("{:?}", calculate(7));
    println!("{:?}", calculate(9));
}
