defmodule Check do
  def x do
    my_data = %{
        # A JSONC input case with both comment forms.
        "url" => "https://example.org/a/*b*/",  # detail
        # continued
        "count" => 2,  # trailing line comment
    }
    _ = my_data
  end
end
