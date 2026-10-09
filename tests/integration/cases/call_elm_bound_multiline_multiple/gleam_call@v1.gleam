pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn f(_value: a) -> Nil { Nil }

pub fn main() {
  let ref_data = GList([
    GInt(1),
    GInt(2),
  ])
  f(GList([
    ref_data,
  ]))
  f(GList([
    ref_data,
  ]))
}
