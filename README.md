Python TCO
----------

An implementation of tail-call optimization in Python, by @lohmataja, @paultag, and @akaptur.

The `make_tail_recusive` decorator replaces the code object of the function that it decorates. The original bytecode is modified to remove `CALL_FUNCTION` bytes and replace them with jumps to the top of the bytecode.
