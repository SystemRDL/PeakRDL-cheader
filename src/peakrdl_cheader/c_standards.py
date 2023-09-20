from typing import Dict
import enum

class CStandard(enum.Enum):

    def __init__(self, version: int, d: Dict[str, bool]) -> None:
        self.anon_unions = d.get("anon_unions", False)
        self.static_assert = d.get("static_assert", False)
        self.static_assert_needs_assert_h = d.get("static_assert_needs_assert_h", False)

        # Prevent Enum from flattening members into aliases
        self._value_ = version

    gnu23 = 23, {
        "anon_unions": True,
        "static_assert": True,
    }

    gnu17 = 17, {
        "anon_unions": True,
        "static_assert": True,
        "static_assert_needs_assert_h": True,
    }

    gnu11 = 11, {
        "anon_unions": True,
        "static_assert": True,
        "static_assert_needs_assert_h": True,
    }

    gnu99 = 99, {}

    gnu90 = 90, {}

    gnu89 = 89, {}

    latest = gnu17 # gnu23 is still unreleased
