def main():
    var my_data: List[String] = List([
        "prefix ${HOME} suffix",
        "${interpolated}",
    ])
    _ = my_data
