defmodule Check do
  def x do
    my_data = %{
        "rows" => {%{"x" => 1, "y" => "a"}, %{"x" => 2, "y" => "b"}},
    }
    _ = my_data
  end
end
