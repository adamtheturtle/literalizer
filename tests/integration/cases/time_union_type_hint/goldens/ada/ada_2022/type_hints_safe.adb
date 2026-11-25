with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("mixed", AList'[AList'[AStr ("09:30:00")], AList'[]])
    ];
begin
    null;
end Main;
