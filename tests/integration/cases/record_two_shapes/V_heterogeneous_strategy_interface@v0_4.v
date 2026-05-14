interface IVal {}

fn main() {
	my_data := {
		'user': {'id': IVal(1), 'name': IVal('Alice')},
		'project': {'title': IVal('report'), 'tags': IVal(['draft', 'urgent'])},
	}
	_ = my_data
}
