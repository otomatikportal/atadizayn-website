# Atadizayn Website

## Local Development

Ensure your .env contains the required settings for your environment.

## Media and Static

Static files are served locally and in production via Whitenoise from the VPS.

Media files are stored locally in development and in Cloudflare R2 via S3 in production.

## Frontend (Bootstrap Customizer)

The Bootstrap custom build lives in frontend/ and outputs to static/css/.

Install dependencies:

- npm install (from frontend/)

Build CSS manually:

- npm run build:css (from frontend/)

When running collectstatic, the CSS build runs automatically.

## Theming

This project uses a custom Bootstrap SCSS build.

### Entry point

- frontend/src/custom.scss imports the partials in frontend/src/scss/.

### SCSS files and responsibilities

- frontend/src/custom.scss: Entry file; wires all partials in order.
- frontend/src/scss/settings.scss: Design tokens and Bootstrap variable overrides.
- frontend/src/scss/bootstrap-stack.scss: Bootstrap core imports (functions, variables, components).
- frontend/src/scss/mixins.scss: Shared custom mixins used by component overrides.
- frontend/src/scss/components.scss: Component-level styling customizations.

### Build output

- The compiled CSS is written to static/css/bootstrap-custom.css.

### Commands

Run from the frontend/ folder:

- npm install
- npm run build:css
- npm run watch:css
