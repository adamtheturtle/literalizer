defmodule Playlist do
  def new(), do: 42
end

defmodule Check do
  def x() do
p = Playlist.new()
if p != 42, do: raise("Expected constructor result")
  end
end
