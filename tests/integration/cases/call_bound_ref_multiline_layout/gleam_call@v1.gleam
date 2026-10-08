pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn f(_value: a) -> Nil { Nil }

pub fn main() {
  let x = GList([
    GList([
      GInt(1),
      GInt(2),
    ]),
    GList([
      GInt(3),
      GInt(4),
    ]),
  ])
  f(GList([
    GList([
      x,
    ]),
  ]))
}
