pub type GVal {
  GInt(Int)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}
pub fn consume(_items: a, _mapping: b) -> Nil { Nil }

pub fn main() {
  let foo = GInt(42)
  consume(GList([
    GDict([
      #("other", GInt(1)),
    ]),
    foo,
  ]), GDict([
    #("left", foo),
    #("other", GInt(1)),
  ]))
}
