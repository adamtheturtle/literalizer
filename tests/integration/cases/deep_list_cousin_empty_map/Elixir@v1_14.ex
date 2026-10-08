defmodule Check do
  def x do
    my_data = [
        %{"items" => [%{"inner" => %{"x" => 1}}, %{"inner" => %{}}]},
        %{"items" => [%{"inner" => %{"x" => 2}}, %{"inner" => %{}}]},
    ]
    _ = my_data
  end
end
