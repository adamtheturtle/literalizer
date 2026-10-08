with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a", AList'[AInt (1), AList'[]])
    ];
begin
    null;
end Main;
