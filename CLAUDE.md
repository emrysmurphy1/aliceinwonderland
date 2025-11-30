# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a TypeScript Node.js project using ES modules. The project uses modern TypeScript 5.3+ with strict type checking enabled.

## Development Commands

### Building
- `npm run build` - Compile TypeScript to JavaScript (output: `dist/`)
- `npm run build:watch` - Watch mode compilation
- `npm run typecheck` - Type check without emitting files

### Running
- `npm run dev` - Run development server with hot reload using `tsx`
- `npm start` - Run the compiled JavaScript from `dist/`

### Testing
- `npm test` - Run all tests with Vitest
- `npm run test:watch` - Run tests in watch mode
- `npm run test:ui` - Open Vitest UI for interactive testing
- To run a single test file: `npx vitest run tests/example.test.ts`
- To run tests matching a pattern: `npx vitest run -t "pattern"`

### Code Quality
- `npm run lint` - Check code with ESLint
- `npm run lint:fix` - Auto-fix linting issues
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check formatting without modifying files

## Project Structure

```
aliceinwonderland/
├── src/           # Source TypeScript files
│   └── index.ts   # Main entry point
├── tests/         # Test files (*.test.ts)
├── dist/          # Compiled JavaScript output (gitignored)
└── node_modules/  # Dependencies (gitignored)
```

## Key Configuration

- **TypeScript**: Strict mode enabled with ES2022 target
- **Module System**: ES modules (`"type": "module"` in package.json)
- **Testing**: Vitest with Node environment
- **Linting**: ESLint with TypeScript support
- **Formatting**: Prettier with 100 character line width, single quotes

## Development Notes

- Source files are in `src/`, compiled output goes to `dist/`
- Use ES module syntax (`import`/`export`, not `require`)
- All source files should use `.ts` extension
- Test files use `.test.ts` extension and live in `tests/` directory
- The project uses strict TypeScript - all types must be properly defined
