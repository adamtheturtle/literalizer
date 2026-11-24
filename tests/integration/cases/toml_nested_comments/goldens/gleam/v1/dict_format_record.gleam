pub type GVal1 {
  GVal1(first: Int, second: Int)
}
pub type GVal2 {
  GVal2(name: String)
}
pub type GVal3 {
  GVal3(inner: Int)
}
pub type GVal0 {
  GVal0(dotted: GVal1, plain: Int, entries: List(GVal2), table: GVal3)
}

pub fn main() {
  let my_data = GVal0(
    dotted: GVal1(
      first: 1,
      second: 2,
    ),
    plain: 3,
    entries: [
      GVal2(
        name: "one",
      ),
      GVal2(
        name: "two",
      ),
    ],
    table: GVal3(
      inner: 4,
    ),
  )
  let _ = my_data
}
