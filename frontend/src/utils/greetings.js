const greetings = [
  "hi",
  "hello",
  "hey",
  "good morning",
  "good afternoon",
  "good evening",
  "thanks",
  "thank you",
  "bye"
];

export function isGreeting(text) {
  const msg = text.trim().toLowerCase();
  return greetings.includes(msg);
}