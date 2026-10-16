module Main

type Val =
    | FNull
let item: Val = FNull
let my_data: Val = FNull
(void)my_data;
let my_data: Val = item
(void)my_data;
