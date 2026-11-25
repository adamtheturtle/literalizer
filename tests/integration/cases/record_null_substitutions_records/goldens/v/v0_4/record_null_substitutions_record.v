struct Record0 {
	due_date int
	parent_id int
	assignee string
}

fn main() {
	my_data := [
		Record0{ due_date: -1, parent_id: -1, assignee: '' },
		Record0{ due_date: 10, parent_id: 20, assignee: 'alice' },
	]
	_ = my_data
}
