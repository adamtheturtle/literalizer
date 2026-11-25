with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val) is begin null; end Process;
    untyped_value : A_Val := AList'[];
begin
    Process(data => AList'[untyped_value, untyped_value]);
end Main;
