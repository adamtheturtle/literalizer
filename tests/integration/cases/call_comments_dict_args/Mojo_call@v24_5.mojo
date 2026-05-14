def process(value: Dict[String, String]):
    pass
def main():
    # Test cases
    process({"type": "create", "pr_id": "pr_1"})  # first case
    process({"type": "update", "pr_id": "pr_2"})  # second case
    # third case
    process({"type": "delete", "pr_id": "pr_3"})
