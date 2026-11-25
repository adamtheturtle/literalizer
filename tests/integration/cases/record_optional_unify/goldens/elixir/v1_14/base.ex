defmodule Check do
  def x do
    my_data = %{
        "items" => [%{"id" => 1}, %{"id" => 2, "count" => 10}, %{"id" => 3, "count" => 20}],
    }
    _ = my_data
  end
end
