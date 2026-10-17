interface IVal {}
interface ICallArg_ {}
struct ThingType_ {}
fn (r ThingType_) go(arg0 ICallArg_, arg1 ICallArg_, arg2 ICallArg_) ICallArg_ { return 0 }

fn main() {
	thing := ThingType_{}
	thing.go([]IVal{}, [IVal(1)], []IVal{});
	thing.go([IVal('text')], [IVal(2)], []IVal{});
	thing.go([]IVal{}, [IVal('text')], []IVal{});
	thing.go([IVal('text')], [IVal(2)], [IVal(3)]);
}
