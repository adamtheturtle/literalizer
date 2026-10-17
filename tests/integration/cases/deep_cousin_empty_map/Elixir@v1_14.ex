defmodule Check do
  def x do
    my_data = [
        %{"outer" => %{"inner" => %{"x" => 1}}},
        %{"outer" => %{"inner" => %{}}},
    ]
    _ = my_data
  end
end
