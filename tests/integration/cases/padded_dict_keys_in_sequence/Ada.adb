procedure Check is
   my_data : A_Val := AList'(
       AMap'(AEntry ("first", AStr ("Alice")), AEntry ("last", AStr ("Smith")), AEntry ("middle", AStr ("Jane"))),
       AMap'(AEntry ("first", AStr ("Bob")), AEntry ("last", AStr ("Jones")))
   );
begin
   null;
end Check;
