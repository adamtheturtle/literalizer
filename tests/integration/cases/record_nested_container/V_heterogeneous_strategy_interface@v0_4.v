interface IVal {}

fn main() {
	my_data := {
		'title': IVal('report'),
		'tags': IVal(['draft', 'urgent', 'review']),
		'priority': IVal(2),
	}
	_ = my_data
}
