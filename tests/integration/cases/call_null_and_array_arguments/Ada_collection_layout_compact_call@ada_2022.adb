with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Value : A_Val) is begin null; end Process;
begin
    Process(value => ANull);
    Process(value => AList'[AInt (1), AInt (2)]);
end Main;
