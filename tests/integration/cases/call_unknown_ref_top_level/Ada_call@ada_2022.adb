with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val) is begin null; end Process;
    unknown_value : A_Val := AList'[];
begin
    Process(data => unknown_value);
end Main;
