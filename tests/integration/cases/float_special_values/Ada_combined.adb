with A_Stub; use A_Stub;
procedure Check is
   my_data : A_Val := AList'[
       AFloat (1.0 / 0.0),
       AFloat (-1.0 / 0.0),
       AFloat (0.0 / 0.0)
   ];
begin
   my_data := AList'[
       AFloat (1.0 / 0.0),
       AFloat (-1.0 / 0.0),
       AFloat (0.0 / 0.0)
   ];
end Check;
