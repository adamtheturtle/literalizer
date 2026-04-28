defmodule Check do
  def process(_data, _count), do: nil
  def x do
    my_var = [
        1,
        2,
        3,
    ]
    my_other = [
        4,
        5,
        6,
    ]
    process(my_var, 42)
    process(my_other, 7)
  end
end
