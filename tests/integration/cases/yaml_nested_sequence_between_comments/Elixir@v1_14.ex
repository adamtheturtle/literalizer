defmodule Check do
  def x do
    my_data = [
        [
            %{"item" => "existing"},
            "kept",
            # This comment trails the first pair.
        ],
        [%{"item" => "next"}, "also kept"],
        # This comment describes the last pair.
        [%{"item" => "last"}, "kept too"],
    ]
    _ = my_data
  end
end
