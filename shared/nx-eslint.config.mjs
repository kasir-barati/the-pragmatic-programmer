// @ts-check

import nx from '@nx/eslint-plugin';
import vitest from '@vitest/eslint-plugin';
import importPlugin from 'eslint-plugin-import';
import perfectionist from 'eslint-plugin-perfectionist';
import unusedImports from 'eslint-plugin-unused-imports';

export default [
  ...nx.configs['flat/base'],
  ...nx.configs['flat/typescript'],
  ...nx.configs['flat/javascript'],
  {
    ignores: ['**/dist', '**/out-tsc', '**/vite.config.*.timestamp*'],
  },
  {
    files: ['**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx'],
    plugins: {
      import: importPlugin,
      perfectionist,
      'unused-imports': unusedImports,
    },
    rules: {
      '@nx/enforce-module-boundaries': [
        'error',
        {
          enforceBuildableLibDependency: true,
          allow: ['^.*/eslint(\\.base)?\\.config\\.[cm]?[jt]s$'],
          depConstraints: [
            {
              sourceTag: '*',
              onlyDependOnLibsWithTags: ['*'],
            },
          ],
        },
      ],
      'import/no-duplicates': ['error', { 'prefer-inline': true }],
      'perfectionist/sort-imports': [
        'error',
        {
          type: 'natural',
          order: 'asc',
          newlinesBetween: 1,
        },
      ],
      'perfectionist/sort-named-imports': [
        'error',
        { type: 'natural' },
      ],
      'perfectionist/sort-named-exports': [
        'error',
        { type: 'natural' },
      ],
      'perfectionist/sort-exports': ['error', { type: 'natural' }],
      'perfectionist/sort-enums': ['error', { type: 'natural' }],
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
      'unused-imports/no-unused-imports': 'error',
      'unused-imports/no-unused-vars': [
        'warn',
        {
          vars: 'all',
          varsIgnorePattern: '^_',
          args: 'after-used',
          argsIgnorePattern: '^_',
        },
      ],
      'no-console': 'error',
      'no-restricted-syntax': [
        'error',
        {
          selector:
            'ExportAllDeclaration[source.value=/\\.spec(\\.|$)/]',
          message: 'Do not re-export spec files from barrel files.',
        },
        {
          selector:
            'ExportNamedDeclaration[source.value=/\\.spec(\\.|$)/]',
          message: 'Do not re-export spec files from barrel files.',
        },
      ],
    },
  },
  {
    files: [
      '**/*.ts',
      '**/*.tsx',
      '**/*.cts',
      '**/*.mts',
      '**/*.js',
      '**/*.jsx',
      '**/*.cjs',
      '**/*.mjs',
    ],
    // Override or add rules here
    rules: {},
  },
  {
    files: ['**/gen-graphql-schema.ts'],
    rules: {
      'no-console': 'off',
    },
  },
  {
    files: ['**/*.config.ts', 'apps/frontend-e2e/src/**/*.ts'],
    rules: {
      '@typescript-eslint/no-namespace': 'off',
      '@typescript-eslint/no-empty-interface': 'off',
      '@typescript-eslint/no-empty-object-type': 'off',
    },
  },
  {
    files: ['**/*.spec.*', '**/*.test.*'],
    rules: {
      'no-restricted-syntax': [
        'error',
        {
          selector: 'ExportNamedDeclaration',
          message: 'Do not export from spec/test files.',
        },
        {
          selector: 'ExportDefaultDeclaration',
          message: 'Do not export from spec/test files.',
        },
        {
          selector: 'ExportAllDeclaration',
          message: 'Do not export from spec/test files.',
        },
      ],
    },
  },
  {
    files: [
      '**/*.spec.ts',
      '**/*.spec.tsx',
      '**/*.e2e-spec.ts',
      '**/vitest.setup.ts',
      '**/*-e2e/**/*.ts',
      '**/global-setup.ts',
      '**/*.fixture.ts',
      '**/*.cy.ts',
    ],
    plugins: {
      vitest,
    },
    rules: {
      '@typescript-eslint/no-unused-expressions': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-non-null-assertion': 'off',
      '@typescript-eslint/no-empty-function': 'off',
      'no-async-promise-executor': 'off',
      'no-console': 'off',
      'vitest/no-disabled-tests': 'error',
      'vitest/no-focused-tests': 'error',
    },
  },
  {
    files: ['**/prisma/**/*.ts', '**/prisma/**/*.js', '**/*.js'],
    rules: {
      'no-console': 'off',
    },
  },
];
