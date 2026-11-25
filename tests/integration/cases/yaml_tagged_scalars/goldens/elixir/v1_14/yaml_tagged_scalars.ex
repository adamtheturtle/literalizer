defmodule Check do
  def x do
    my_data = %{
        "explicit_string" => "5",
        "six" => "explicitly tagged key",
    }
    _ = my_data
  end
end
