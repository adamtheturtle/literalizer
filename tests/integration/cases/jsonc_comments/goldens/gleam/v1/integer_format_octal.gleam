pub type GVal {
  GInt(Int)
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // A JSONC input case with both comment forms.
    #("url", GStr("https://example.org/a/*b*/")),  // detail
    // continued
    #("count", GInt(0o2)),  // trailing line comment
  ])
  let _ = my_data
}
