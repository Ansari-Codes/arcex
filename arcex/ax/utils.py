from arcex.ax.Exceptions import AXError

def html(component):
    if hasattr(component, '__html__'):
        return component.__html__()
    raise AXError(f"Cannot generate html because given object of type `{type(component).__name__}` has no `__html__` method")