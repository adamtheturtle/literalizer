defmodule Check do
  def x do
    existing = %{
        "_" => "_",
    }
    my_data = existing
    _ = my_data
  end
end
