with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val) is begin null; end Process;
    my_var : A_Val := AInt (42);
begin
    Process(data => AList'[my_var, AInt (42), AStr ("static")]);
end Main;
