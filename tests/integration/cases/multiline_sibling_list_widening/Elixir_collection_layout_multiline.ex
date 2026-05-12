defmodule Check do
  def x do
    my_data = %{
        "sibling_lists" => %{
            "numbers" => [
                1,
                2,
            ],
            "strings" => [
                "x",
                "y",
            ],
        },
        "ref_marker_present" => [
            "$keep",
            "z",
        ],
    }
    _ = my_data
  end
end
