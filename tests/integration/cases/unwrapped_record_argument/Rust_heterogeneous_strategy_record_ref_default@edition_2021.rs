#[derive(Clone)]
pub struct Record0 {
    pub a: i32,
    pub b: &'static str,
}
fn main() {
    fn consume_widget<A>(_arg_value: A) {}
    consume_widget(Record0 {
        a: 1,
        b: "x",
    });
}
