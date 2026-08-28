Imports System.Collections.Generic
Module Check
    ' About the first dotted key.
    ' About the second dotted key.
    ' About the plain key.
    ' Inside the table.
    ' Before the first entry.
    ' Before the second entry.
    Dim my_data = New Dictionary(Of String, Object) From {
        {"dotted", New Dictionary(Of String, Object) From {{"first", 1}, {"second", 2}}},
        {"plain", 3},
        {"table", New Dictionary(Of String, Object) From {{"inner", 4}}},
        {"entries", New Object() {New Dictionary(Of String, Object) From {{"name", "one"}}, New Dictionary(Of String, Object) From {{"name", "two"}}}}
    }
End Module
