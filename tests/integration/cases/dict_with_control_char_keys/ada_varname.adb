procedure Check is
   my_data : A_Val := AMap'(
       AEntry ("key\nwith\nnewlines", AStr ("value1")),
       AEntry ("key	with	tabs", AStr ("value2"))
   );
begin
   null;
end Check;
