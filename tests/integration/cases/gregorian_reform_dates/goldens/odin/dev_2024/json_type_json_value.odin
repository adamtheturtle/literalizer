#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`{"ancient_date": "1500-03-01", "modern_date": "2024-01-15", "before_date": "1582-10-04", "gap_date": "1582-10-10", "transition_date": "1582-10-15", "after_date": "1582-10-16", "before_naive": "1582-10-04T12:30:00.000001Z", "gap_naive": "1582-10-10T12:30:00.500000Z", "transition_positive": "1582-10-15T00:30:00+18:00", "transition_negative": "1582-10-15T23:30:00-18:00", "after_positive": "1582-10-16T00:30:00+18:00"}`)
_ = my_data
}
