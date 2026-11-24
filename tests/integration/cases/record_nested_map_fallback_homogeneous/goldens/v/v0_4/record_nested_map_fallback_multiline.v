interface IVal {}
struct Record1 {
	kind string
	pr_id string
}
struct Record0 {
	name string
	input Record1
	expected map[string]IVal
}

fn main() {
	my_data := [
		Record0{
			name: 'test_1',
			input: Record1{
				kind: 'create',
				pr_id: 'pr_1',
			},
			expected: {
				'pr_id': IVal('pr_1'),
				'status': IVal('draft'),
			},
		},
		Record0{
			name: 'test_2',
			input: Record1{
				kind: 'publish',
				pr_id: 'pr_1',
			},
			expected: {
				'error': IVal('invalid_operation'),
			},
		},
	]
	_ = my_data
}
