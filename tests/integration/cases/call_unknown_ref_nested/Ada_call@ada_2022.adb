with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Known_Value : A_Val; Nested_Missing : A_Val) is begin null; end Process;
    known_value : A_Val := ABool (True);
    unknown_value : A_Val := ABool (True);
begin
    Process(known_value => known_value, nested_missing => AList'[unknown_value]);
end Main;
