defmodule Check do
  def process(_data, _count), do: nil
  def x do
    repeated_var = 1
    single_var = [
        4,
        5,
        6,
    ]
    process(repeated_var, 1)
    process(single_var, 0)
    process(repeated_var, 8)
  end
end
