with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("rows", AList'[AMap'[AEntry ("x", AInt (1)), AEntry ("y", AStr ("a"))], AMap'[AEntry ("x", AInt (2)), AEntry ("y", AStr ("b"))]])
    ];
begin
    null;
end Main;
