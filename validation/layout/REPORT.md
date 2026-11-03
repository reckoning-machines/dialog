# Workspace layout

Dialog now uses an inset workspace, compact toolbar, wider primary area, narrow right panel, and connected table/grid sections. DIALOG uses IRIS's serif wordmark proportions. The existing slogan and palette remain. IRIS was inspected read-only; its code and application were not changed.

Browser checks passed at 1440, 900 and 390 pixels, including the evidence drawer, no horizontal overflow and no script errors. The populated workspace uses a retained step-15 snapshot for visual inspection only; mutation requests were blocked. The live desk revision did not change. Stable mobile viewport captures were inspected separately from full-page capture.

Only layout/brand markup and CSS changed. The embedded JavaScript is byte-identical to the application-tested version. Research, portfolio, authority, accounts and action behavior are unchanged. [Evidence and surface hashes](../../evidence/layout-20261103).

`audit.py` verifies the original application evidence, current executable/configuration bytes, the separately checked surface, and the B-02 archive. Markdown remains documentary material; current editorial changes are not asserted to be the old test snapshot.
