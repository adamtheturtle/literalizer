with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val) is begin null; end Process;
begin
    Process(data => AList'[AInt (1), AStr ("x")]);
end Main;
