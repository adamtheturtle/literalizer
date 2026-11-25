interface IVal {}
struct Record0 {
	name string
	input map[string]IVal
	expected map[string]IVal
}

fn main() {
	my_data := [
		Record0{ name: 'test_1', input: {'type': IVal('create'), 'pr_id': IVal('pr_1'), 'draft': IVal(true), 'missing': IVal(unsafe { nil })}, expected: {'pr_id': IVal('pr_1'), 'status': IVal('draft')} },
		Record0{ name: 'test_2', input: {'type': IVal('publish'), 'pr_id': IVal('pr_1')}, expected: {'error': IVal('invalid_operation')} },
	]
	_ = my_data
}
