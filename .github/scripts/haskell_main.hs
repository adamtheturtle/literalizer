module Main where

import Check

main :: IO ()
main = seq Check.my_data (return ())
