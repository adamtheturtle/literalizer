defmodule Check do
  def x do
    my_data = MapSet.new([
        0o1,
        0o20000000000000,
    ])
    _ = my_data
  end
end
