defmodule Check do
  def x do
    my_data = %{
        "a" => [%{}, %{"x" => 1}],
        "b" => [[], [1]],
    }
    _ = my_data
  end
end
