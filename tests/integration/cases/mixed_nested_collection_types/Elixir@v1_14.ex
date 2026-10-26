defmodule Check do
  def x do
    my_data = %{
        "lists" => [[1], ["x"], []],
        "maps" => [%{"x" => 1}, %{"x" => "s"}],
        "empties" => %{"a" => [1], "b" => []},
    }
    _ = my_data
  end
end
