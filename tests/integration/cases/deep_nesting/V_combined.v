interface IVal {}

fn main() {
	mut my_data := {
		'level1': {'level2': IVal({'level3': IVal({'level4': {'value': IVal('deep'), 'items': IVal(['a', 'b'])}}), 'sibling': IVal(42)}), 'tags': IVal([{'name': IVal('tag1'), 'meta': IVal({'priority': IVal(1), 'labels': IVal(['x', 'y'])})}])},
	}
	my_data = {
		'level1': {'level2': IVal({'level3': IVal({'level4': {'value': IVal('deep'), 'items': IVal(['a', 'b'])}}), 'sibling': IVal(42)}), 'tags': IVal([{'name': IVal('tag1'), 'meta': IVal({'priority': IVal(1), 'labels': IVal(['x', 'y'])})}])},
	}
	_ = my_data
}
