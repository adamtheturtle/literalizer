defmodule Check do
  def x do
    my_data = %{
        "key" => "\"bang!\"",  # real
    }
    _ = my_data
  end
end
