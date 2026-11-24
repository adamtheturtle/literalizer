interface IVal {}

fn main() {
	my_data := [
		{'input': {'kind': IVal('add'), 'item_id': IVal('item_1'), 'urgent': IVal(true)}, 'expected': {'item_id': IVal('item_1'), 'state': IVal('pending')}},
		{'input': {'kind': IVal('remove'), 'item_id': IVal('item_9')}, 'expected': {'error': IVal('not_found')}},
	]
	_ = my_data
}
