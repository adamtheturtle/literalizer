interface ICallArg_ {}
struct FooType_ {}
fn (r FooType_) class(arg0 ICallArg_) {}

fn main() {
	foo := FooType_{}
	foo.class(1);
}
