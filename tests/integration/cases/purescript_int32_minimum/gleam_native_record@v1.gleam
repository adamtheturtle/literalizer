pub type GVal0 {
  GVal0(minimum: Int, neighbor: Int, maximum: Int, nested: List(Int))
}

pub fn main() {
  let my_data = GVal0(
    minimum: -2147483648,
    neighbor: -2147483647,
    maximum: 2147483647,
    nested: [
      -2147483648,
    ],
  )
  let _ = my_data
}
