defmodule Check do
  def x do
    my_data = %{
        "not-a-field" => 1,
    }
    _ = my_data
  end
end
