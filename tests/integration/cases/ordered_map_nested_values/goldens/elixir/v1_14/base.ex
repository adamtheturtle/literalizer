defmodule Check do
  def x do
    my_data = %{
        "ordered" => [
            # ordered entry
            {"name", "Alice"},
            {"scores", %{
                # score meaning
                1 => "first",
                2 => "second",  # latest score
            }},
        ],
    }
    _ = my_data
  end
end
