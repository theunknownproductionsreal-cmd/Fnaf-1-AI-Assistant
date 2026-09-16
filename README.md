# FNaF 1 AI Assistant & Dispatcher Engine

A high-performance local dispatcher tool for Five Nights at Freddy's 1, built for Termux and low-resource mobile environments. Combines deterministic game data, regex overrides, zero-latency python blocklists, and a local Ollama integration (Llama 3.2 1B).

## Features
- **Exact AI Mechanics:** Accurate interval timings, movement loop mechanics, lore, and easter egg breakdowns for Nights 1–6 and 4/20 Mode.
- **Guardrailed Local LLM:** Built-in Python blocklist and regular expressions that filter out hoaxes, fan memes, and fake game code before local model inference.
- **ANSI ASCII Art Gallery:** Colored terminal output for main animatronics (Bonnie, Freddy, Chica, Foxy, Golden Freddy).

## Requirements
- Python 3.x
- [Ollama](https://ollama.com) with `llama3.2:1b` model pulled locally (`ollama run llama3.2:1b`)

## Usage
```bash
python fnaf1_dispatcher.py
cat << 'EOF' > LICENSE
MIT License
​Copyright (0) 2026 theunknownproductionsreal-cmd
​Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
​The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
​THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
