with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Values : A_Val; Count : A_Val) is begin null; end Process;
begin
    Process(values => AList'[AInt (1), AMap'[]], count => AInt (42));
end Main;
