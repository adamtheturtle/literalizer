defmodule Check do
  def x do
    my_data = MapSet.new([
        1.5,
        9007199254740993,
    ])
    _ = my_data
  end
end
