func consume(rows []Record0) {
	if len(rows) != 2 {
		panic("record count changed")
	}
	var first map[string]any = rows[0].Attributes
	second := rows[1].Attributes
	if len(first) != 2 || len(second) != 1 ||
		rows[0].Name != "row_3" || first["colour"] != "green" ||
		first["size"] != "small" || rows[1].Name != "row_4" ||
		second["colour"] != "white" {
		panic("record values changed")
	}
}
