defmodule Playlist do
  def new(), do: 42
end

defmodule Check do
  def x() do
P = 'Playlist'(),
if p != 42, do: raise("Expected constructor result")
  end
end
