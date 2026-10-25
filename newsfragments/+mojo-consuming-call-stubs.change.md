Mojo call stubs now accept ownership of their arguments, so references listed in `consumable_refs` can transfer their values to the generated stub.
References outside `consumable_refs` retain their existing formatting.
