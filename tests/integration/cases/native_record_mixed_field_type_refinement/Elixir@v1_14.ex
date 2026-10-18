defmodule Check do
  def x do
    my_data = %{
        "first" => %{"items" => [1, %{"value" => 2}]},
        "second" => %{"items" => [1, %{"value" => "s"}]},
    }
    _ = my_data
  end
end
