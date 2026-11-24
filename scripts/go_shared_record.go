package main

import (
	"encoding/json"
	"os"
)

func consume(declaring, dependent, repeated []Record0) {
	if len(dependent) == 0 || len(dependent) != len(repeated) || &dependent[0] != &repeated[0] {
		panic("repeated reference lost its backing array")
	}
	records := map[string][]Record0{
		"declaring": declaring,
		"dependent": dependent,
	}
	documents := make(map[string][]map[string]any, len(records))
	for document, rows := range records {
		values := make([]map[string]any, 0, len(rows))
		for _, row := range rows {
			values = append(values, map[string]any{
				"name":       row.Name,
				"attributes": row.Attributes,
			})
		}
		documents[document] = values
	}
	encoder := json.NewEncoder(os.Stdout)
	if err := encoder.Encode(documents); err != nil {
		panic(err)
	}
}
