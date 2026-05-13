let Value = < Int : Integer | Str : Text > in
let my_data = {
  omap_value = {first = +1},
  sibling_lists = {numbers = [Value.Int +1, Value.Int +2], strings = [Value.Str "x", Value.Str "y"]},
  ref_marker_present = ["\$keep", "z"],
} in my_data
