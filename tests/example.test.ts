import { describe, it, expect } from 'vitest';
import { main } from '../src/index';

describe('main', () => {
  it('should run without errors', () => {
    expect(() => main()).not.toThrow();
  });
});
