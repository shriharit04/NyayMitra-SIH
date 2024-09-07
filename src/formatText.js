export function formatText(text, wordsPerLine = 14) {
    const words = text.split(' ');
    const lines = [];

    for (let i = 0; i < words.length; i += wordsPerLine) {
      lines.push(words.slice(i, i + wordsPerLine).join(' '));
    }

    return lines.join('<br/>'); // Use <br/> to add line breaks in HTML
  }
