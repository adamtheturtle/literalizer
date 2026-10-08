defmodule Check do
  def x do
    my_data = %{
        "x" => "=",
        # unrelated
    }
    _ = my_data
  end
end
