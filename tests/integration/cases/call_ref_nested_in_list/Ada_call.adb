with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val) is begin null; end Process;
    my_var : A_Val := AInt (42);
    my_other : A_Val := AInt (7);
begin
    Process(data => AList'[AMap'[AEntry ("ref", AStr ("my_var"))], AInt (42), AStr ("static")]);
    Process(data => AList'[AMap'[AEntry ("ref", AStr ("my_other"))], AInt (7), AStr ("label")]);
end Main;
