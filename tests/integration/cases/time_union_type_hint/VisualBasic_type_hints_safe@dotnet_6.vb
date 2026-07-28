Imports System
Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"mixed", New TimeOnly()() {New TimeOnly() {New TimeOnly(9, 30, 0)}, New TimeOnly() {}}}
    }
End Module
