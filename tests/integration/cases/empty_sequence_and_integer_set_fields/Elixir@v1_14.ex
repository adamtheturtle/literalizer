defmodule Check do
  def x do
    my_data = %{
        "a" => [],
        "b" => MapSet.new([1, 2]),
    }
    _ = my_data
  end
end
