with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AStr ("1970-01-01T00:00:00.000001+00:00"),
        AStr ("1969-12-31T23:59:59.500000+00:00"),
        AStr ("1970-01-01T00:00:01+00:00")
    ];
begin
    null;
end Main;
