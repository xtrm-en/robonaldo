from . import context

ctx = context()

print(ctx)

l = ["a", "b"]
print(ctx.join(l))