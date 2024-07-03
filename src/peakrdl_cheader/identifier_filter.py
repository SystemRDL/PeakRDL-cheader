
C_KEYWORDS = {
    # Base
    "auto", "break", "case", "char", "const", "continue", "default", "do",
    "double", "else", "enum", "extern", "float", "for", "goto", "if", "int",
    "long", "register", "return", "short", "signed", "sizeof", "static",
    "struct", "switch", "typedef", "union", "unsigned", "void", "volatile",
    "while",

    # C99
    "inline", "restrict", "_Bool", "_Complex", "_Imaginary",

    # C11
    "_Alignas", "_Alignof", "_Atomic", "_Generic", "_Noreturn",
    "_Static_assert", "_Thread_local",

    # C23
    "alignas", "alignof", "bool", "constexpr", "false", "nullptr",
    "static_assert", "thread_local", "true", "typeof", "typeof_unqual",
    "_BitInt", "_Decimal128", "_Decimal32", "_Decimal64",
}

def kw_filter(s: str) -> str:
    """
    Make all user identifiers 'safe' and ensure they do not collide with
    C keywords.

    If a C keyword is encountered, add an underscore suffix
    """
    if s in C_KEYWORDS:
        s += "_"
    return s
