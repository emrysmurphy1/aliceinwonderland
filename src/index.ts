export function main() {
  console.log('Welcome to Wonderland!');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
