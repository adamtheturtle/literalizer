module Check where


import Prelude
data Val
    = PFloat Number


std :: Val
std = PFloat (0.0 / 0.0)
