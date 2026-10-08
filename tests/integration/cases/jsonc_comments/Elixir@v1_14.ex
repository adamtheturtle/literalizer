defmodule Check do
  def x do
    my_data = %{
        "url" => "https://example.org/a/*b*/",
        "count" => 2,
    }
    _ = my_data
  end
end
