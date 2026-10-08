defmodule Check do
  def x do
    my_data = %{
        "text" => "a\"//b",
    }
    _ = my_data
  end
end
