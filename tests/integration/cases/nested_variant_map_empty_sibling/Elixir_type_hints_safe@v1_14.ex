defmodule Check do
  def x do
    my_data = [
        %{"nested" => %{"count" => 1, "name" => "value"}},
        %{},
    ]
    _ = my_data
  end
end
