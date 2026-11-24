defmodule Check do
  def x do
    my_data = %{
        "value" => %{"$ref" => "foo"},
    }
    _ = my_data
  end
end
