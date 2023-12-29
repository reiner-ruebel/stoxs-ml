from app.core.extensions.extensions_v1 import extensions

def get_extension(extension_name: str) -> object:
    """Returns an extension by its name."""
        
    for name, ext_object, _, _ in extensions:
        if name == extension_name:
            return ext_object

    raise ValueError(f"Extension '{extension_name}' not found")
