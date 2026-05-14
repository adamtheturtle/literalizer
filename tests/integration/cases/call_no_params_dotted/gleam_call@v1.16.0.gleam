pub type GVal {
  GList(List(GVal))
}
pub fn throttler_check() -> Nil { Nil }

pub fn main() {
  throttler_check()
  throttler_check()
}
