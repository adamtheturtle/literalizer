interface IVal {}

fn main() {
	mut my_data := [
		{'type': IVal('create'), 'pr_id': IVal('pr_1'), 'draft': IVal(true)},
		{'type': IVal('create'), 'pr_id': IVal('pr_2')},
	]
	my_data = [
		{'type': IVal('create'), 'pr_id': IVal('pr_1'), 'draft': IVal(true)},
		{'type': IVal('create'), 'pr_id': IVal('pr_2')},
	]
	_ = my_data
}
