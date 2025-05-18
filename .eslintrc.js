module.exports = {
  root: true,
  env: {
    browser: true,
    es2020: true,
    node: true,
    jest: true,
  },
  plugins: ['jsdoc', 'react-refresh'],
  extends: [
    'airbnb',
    'airbnb/hooks',
    'eslint:recommended',
    'plugin:jsdoc/recommended',
    'plugin:react/recommended',
    'plugin:react/jsx-runtime',
    'plugin:react-hooks/recommended',
    'plugin:cypress/recommended',
    'prettier',
  ],
  ignorePatterns: ['dist', '.eslintrc.js'],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  settings: { react: { version: '18.2' } },
  rules: {
    'react/jsx-no-target-blank': 'off',
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
  overrides: [
    {
      files: ['.eslintrc.{js,cjs}'],
      env: {
        node: true,
      },
      parserOptions: {
        sourceType: 'script',
      },
    },
    {
      files: ['*.json'],
      extends: ['plugin:json/recommended', 'plugin:json/prettier'],
      parser: 'jsonc-eslint-parser',
    },
    {
      files: ['*.jsonc'],
      extends: ['plugin:jsonc/recommended-with-jsonc', 'plugin:jsonc/prettier'],
      parser: 'jsonc-eslint-parser',
    },
    {
      files: ['*.json5'],
      extends: ['plugin:jsonc/recommended-with-json5', 'plugin:jsonc/prettier'],
      parser: 'jsonc-eslint-parser',
    },
    {
      files: ['cypress.config.js', 'cypress/**/*.js'],
      rules: {
        'import/no-extraneous-dependencies': [
          'error',
          { devDependencies: true },
        ],
      },
    },
    {
      files: ['**/*.{js,mjs,cjs,jsx}'],
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
        globals: {
          ...require('globals').browser,
          ...require('globals').node,
        },
      },
    },
  ],
};
