with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[AList'[AMap'[AEntry ("$ref", AStr ("my_var"))], AInt (42), AStr ("static")]],
        AList'[AList'[AMap'[AEntry ("$ref", AStr ("my_other"))], AInt (7), AStr ("label")]]
    ];
begin
    null;
end Main;
