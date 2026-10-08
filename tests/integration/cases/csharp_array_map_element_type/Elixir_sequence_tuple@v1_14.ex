defmodule Check do
  def x do
    my_data = %{
        "d" => {%{"a" => {%{"b" => {1, {2.5, {"x", {true}}}}}}}},
    }
    _ = my_data
  end
end
