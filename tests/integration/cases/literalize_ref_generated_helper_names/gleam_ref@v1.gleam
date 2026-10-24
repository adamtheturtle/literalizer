pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let std = GDict([
    #("a", GInt(1)),
  ])
  let arena = GDict([
    #("a", GInt(1)),
  ])
  let allocator = GDict([
    #("a", GInt(1)),
  ])
  let my_data = GList([
    std,
    arena,
    allocator,
  ])
  let _ = my_data
}
