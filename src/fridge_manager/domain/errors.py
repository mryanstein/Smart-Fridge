class DomainError(Exception):
    """Klasa bazowa błędów domenowych."""
    pass


class IncompatibleUnitError(DomainError):
    """Jednostek nie da się przeliczyć."""
    pass


class InvalidQuantityError(DomainError):
    """Nieprawidłowa ilość produktu."""
    pass


class InsufficientStockError(DomainError):
    """Niewystarczająca ilość produktu w lodówce."""
    pass

class InvalidProductNameError(DomainError):
    """Nieprawidłowa nazwa produktu."""
    pass


class InvalidUnitError(DomainError):
    """Nieprawidłowa jednostka produktu."""
    pass
