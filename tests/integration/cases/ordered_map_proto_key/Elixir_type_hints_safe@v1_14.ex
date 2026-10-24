defmodule Check do
  def x do
    my_data = [
        {"__proto__", %{"x" => 1}},
        {"ordinary", 2},
    ]
    _ = my_data
  end
end
