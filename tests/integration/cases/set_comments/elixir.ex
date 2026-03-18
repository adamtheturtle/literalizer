defmodule Check do
  def x do
    MapSet.new([
    "apple",  # inline comment
    # before banana
    "banana",
    # trailing
])
  end
end
