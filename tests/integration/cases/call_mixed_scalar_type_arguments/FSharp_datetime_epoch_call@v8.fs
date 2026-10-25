module Main

type Val =
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FDate of System.DateOnly
    | FInt of int64
let capture (_nan_value: obj, _positive_infinity: obj, _negative_infinity: obj, _finite_value: obj, _date_value: obj, _datetime_value: obj, _text_value: obj) : obj = null
capture(FFloat nan, FFloat infinity, FFloat(-infinity), FFloat 1.25, FDate (System.DateOnly(2024, 1, 15)), FInt 1705322096L, FStr "[ordinary text]") |> ignore
