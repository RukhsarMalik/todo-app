import nextPlugin from "eslint-config-next";
import tseslint from "typescript-eslint";

export default tseslint.config(
  nextPlugin.configs["core-web-vitals"],
  {
    files: ["**/*.ts", "**/*.tsx"],
    // tsconfig.json is required for the `no-floating-promises` rule
    languageOptions: {
      parserOptions: {
        project: true,
      },
    },
  },
  {
    ignores: [
      ".next/**",
      "out/**",
      "build/**",
      "node_modules/",
      "next-env.d.ts",
      "*.config.js",
      "eslint.config.mjs"
    ],
  }
);