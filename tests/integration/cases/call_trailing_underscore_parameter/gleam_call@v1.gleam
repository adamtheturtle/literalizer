pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn do_thing(_x_: a) -> Nil { Nil }

pub fn main() {
  let _ = do_thing(GInt(1))
  let _ = do_thing(GInt(2))
}
