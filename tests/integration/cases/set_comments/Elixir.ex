defmodule Check do
  def my_data do
    MapSet.new([
    "apple",  # inline comment
    # before banana
    "banana",
    # trailing
])
  end
end
