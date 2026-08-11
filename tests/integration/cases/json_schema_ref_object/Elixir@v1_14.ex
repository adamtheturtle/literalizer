defmodule Check do
  def x do
    my_data = %{
        "schema" => %{"$ref" => "#/defs/Foo"},
    }
    _ = my_data
  end
end
