with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
begin
    -- Test cases
    Process(value => AStr ("hello"));  -- single word
    Process(value => AStr ("hello world"));  -- two words
    -- trailing comment
end Main;
