with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AMap'[AEntry ("key", AMap'[AEntry ("$ref", AStr ("my_var"))]), AEntry ("count", AInt (42))]]
    ];
begin
    null;
end Main;
