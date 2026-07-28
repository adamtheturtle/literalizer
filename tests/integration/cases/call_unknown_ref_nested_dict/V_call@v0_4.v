interface IVal {}
interface ICallArg_ {}
fn process(args ...ICallArg_) {}

fn main() {
	my_list := {
		'unused': 'value',
	}
	process([[{'inner': my_list}]]);
}
