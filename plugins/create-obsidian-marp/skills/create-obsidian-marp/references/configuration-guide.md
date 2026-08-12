# Marp configuration choices

## Defaults and available values

| Setting | Default | Available values | Meaning |
|---|---|---|---|
| Theme | `default` | Built-ins: `default`, `gaia`, `uncover`; detected local theme IDs | Typography, colors, spacing, visual design |
| Custom styling | None | Theme only; inline `style: \|`; confirmed local theme CSS | Theme overrides or extensions |
| Slide size | `16:9` | `16:9`; `4:3`; names defined by selected theme | Aspect ratio and canvas |
| Pagination | On | On; Off | Slide numbers |
| Header/footer | None | None; header; footer; both | Repeated text |
| Images | Local or approved | None; local; approved remote; both | Visual dependencies |
| Markdown-it plugins | None | Only detected enabled plugins | Optional syntax |

## Trade-offs

- `default` is neutral and portable; `gaia` is presentation-styled; `uncover` is minimal and spacious.
- `16:9` fits modern displays; `4:3` suits older projectors or square layouts.
- Custom CSS/themes reduce portability.
- Local images work offline but must travel with the vault.
- Remote images require network and stable URLs.
- Plugins fail in vaults without matching configuration.

## Discovery and confirmation

When a target vault exists, inspect it for custom themes and enabled plugins. Never claim unobserved options are installed. Show detected values under **Confirmed local options**. Without inspection, only built-ins are confirmed.

Ask:

> Use the default Marp configuration, or customize it?

Offer:

- **Use defaults**
- **Customize theme**
- **Customize configuration**

Ask one focused follow-up per changed setting. For nonstandard dependencies, confirm availability and portability and record them in a comment when useful.

