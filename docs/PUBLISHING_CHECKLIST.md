# Publishing checklist

The delivered archive contains one repository root. Extract it, then put the
**contents** of that root in the new Git repository. Do not nest an extra copy
inside another repository or upload private working directories with it.

Before pushing:

- Run the three commands in [Validation](VALIDATION.md) from a clean tree.
- Keep `.gitattributes`, `.gitignore` and `.github/` files; they are intentional.
- Review `git diff --stat` and `git diff --cached --stat` before committing.
- Confirm no private images, saves, keys, serials or vendor binaries were added.
- Preserve `.txt` archival warnings and upstream notices.
- Preserve [license scope](../LICENSE_STATUS.md): MIT for original code and CC BY 4.0
  for original documentation, with third-party rights kept separate.
- Do not convert historical device writers into a one-click tool or treat fixed
  block numbers as a portable repair configuration.

GitHub CI validates documentation, indexes and synthetic tests only. It is not a
certification that a hardware operation is safe. Check the public Actions run for the exact commit being published.
