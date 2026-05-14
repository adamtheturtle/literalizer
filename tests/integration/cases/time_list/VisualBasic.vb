Imports System
Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"times", New Object() {New TimeOnly(9, 30, 0), New TimeOnly(17, 45, 0), New TimeOnly(23, 59, 59)}}
    }
End Module
