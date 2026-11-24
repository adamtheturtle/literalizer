defmodule Check do
  def x do
    my_data = %{
        "first" => [[1, "value"], []],
        "second" => [[], [2, "other"]],
    }
    _ = my_data
  end
end
