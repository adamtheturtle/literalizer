Imports System.Collections.Generic
Module Check
    Dim Existing = 1
    Dim my_data = New Object() {
        0,
        New Integer()() {New Integer() {Existing}}
    }
End Module
