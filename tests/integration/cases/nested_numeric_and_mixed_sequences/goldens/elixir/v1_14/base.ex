defmodule Check do
  def x do
    my_data = %{
        "numbers" => [1, 2],
        "nested" => %{"inner" => [3]},
        "mixed" => [4, "five"],
    }
    _ = my_data
  end
end
