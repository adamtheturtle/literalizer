pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    // heading
    #("a", GStr("single ' // data")),
    #("b", GStr("linecontinuation")),
    #("c", GStr("\\")),  // actual comment
    #("d", GStr("    ")),  // final comment
  ])
  let _ = my_data
}
