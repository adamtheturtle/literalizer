defmodule Check do
  def x do
    my_data = [
        [[%{"$ref" => "myVar"}, 42, "static"]],
    ]
    _ = my_data
  end
end
