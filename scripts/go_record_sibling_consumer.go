package main

import (
	"encoding/json"
	"os"
)

func writeSiblingRecords(records []Record0) {
	observed := make([]map[string]any, 0, len(records))
	for _, record := range records {
		switch record.Tag {
		case "empty":
			if record.Items == nil || len(record.Items) != 0 {
				panic("empty sibling must retain an empty slice")
			}
		case "nulls":
			if len(record.Items) != 2 || record.Items[0] != nil || record.Items[1] != nil {
				panic("null-only sibling must retain both nil elements")
			}
		case "mixed":
			if len(record.Items) != 3 {
				panic("mixed sibling must retain all three elements")
			}
			if _, ok := record.Items[0].(int); !ok {
				panic("expected the first mixed item to be an int")
			}
			if _, ok := record.Items[1].(string); !ok {
				panic("expected the second mixed item to be a string")
			}
			if _, ok := record.Items[2].(bool); !ok {
				panic("expected the third mixed item to be a bool")
			}
		default:
			panic("unexpected sibling tag")
		}
		observed = append(observed, map[string]any{"tag": record.Tag, "items": record.Items})
	}
	if err := json.NewEncoder(os.Stdout).Encode(map[string]any{"records": observed}); err != nil {
		panic(err)
	}
}
