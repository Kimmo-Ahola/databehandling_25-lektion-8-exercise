class Utils():
    @staticmethod
    def split_full_name(full_name: str) -> tuple[str | None, str | None]:
        parts = full_name.split()
        first_name = parts[0] if len(parts) > 0 else ""
        last_name = parts[1] if len(parts) > 1 else None

        return first_name, last_name
