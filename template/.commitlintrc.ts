import { UserConfig } from '@commitlint/types';
import { rules as conventionalRules } from '@commitlint/config-conventional';

const defaultTypes = conventionalRules['type-enum'][2] as string[];

const config: UserConfig = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'header-max-length': [1, 'always', 72],
    'type-enum': [2, 'always', [...defaultTypes, 'deps']],
  },
};

export default config;
