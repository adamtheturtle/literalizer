defmodule Check do
  def my_data do
    my_data = MapSet.new([
    true,
    42,
    "apple",
])
    _ = my_data
  end
end
