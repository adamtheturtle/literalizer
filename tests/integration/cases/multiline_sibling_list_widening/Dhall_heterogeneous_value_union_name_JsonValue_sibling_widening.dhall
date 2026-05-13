let JsonValue = < Int : Integer | Str : Text > in
let my_data = {
  omap_value = {first = +1},
  sibling_lists = {numbers = [JsonValue.Int +1, JsonValue.Int +2], strings = [JsonValue.Str "x", JsonValue.Str "y"]},
  ref_marker_present = ["\$keep", "z"],
} in my_data
