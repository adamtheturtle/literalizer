defmodule Check do
  def x do
    my_data = {
        {%{"values" => {{}}}, %{}},
        {%{}, %{"values" => {{}}}},
    }
    _ = my_data
  end
end
