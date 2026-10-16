interface IVal {}
interface ICallArg_ {}
fn make_widget(args ...ICallArg_) ICallArg_ { return 0 }

fn main() {
	make_widget([]IVal{}, [1], []IVal{});
	make_widget(['text'], [2], []IVal{});
	make_widget([]IVal{}, ['text'], []IVal{});
	make_widget(['text'], [2], [3]);
}
