with A_Stub; use A_Stub;
procedure Check is
    my_data : A_Val := AList'[
        AList'[AMap'[AEntry ("name", AStr ("Alice"))], AMap'[AEntry ("name", AStr ("Bob"))]],
        AList'[AMap'[AEntry ("name", AStr ("Charlie"))], AMap'[AEntry ("name", AStr ("Dave"))]]
    ];
begin
    null;
end Check;
