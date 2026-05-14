with A_Stub; use A_Stub;
procedure Main is
    procedure Fetch (Value : A_Val) is begin null; end Fetch;
begin
    Fetch(value => AStr ("hello"));
    Fetch(value => AStr ("world"));
end Main;
