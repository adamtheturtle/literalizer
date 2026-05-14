defmodule Check do
  def x do
    my_data = %{
        "key" => "value \" # not a comment",  # real
    }
    _ = my_data
  end
end
