defmodule Check do
  def x do
    my_data = [
        [[%{"$ref" => "my_var"}, 42, "static"]],
        [[%{"$ref" => "my_other"}, 7, "label"]],
    ]
    _ = my_data
  end
end
