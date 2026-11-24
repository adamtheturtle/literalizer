with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AMap'[AEntry ("a" & Character'Val(9) & "b" & Character'Val(10) & "c", AInt (1)), AEntry ("id", AStr ("x"))]
    ];
begin
    null;
end Main;
