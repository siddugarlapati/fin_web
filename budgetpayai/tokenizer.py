"""
Simple BPE tokenizer for Aiza
"""
import json
import regex as re
from collections import Counter


class AizaTokenizer:
    def __init__(self, vocab_size=10000):
        self.vocab_size = vocab_size
        self.vocab = {}
        self.merges = {}
        self.pattern = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""")
        
    def train(self, texts):
        """Train tokenizer on text data"""
        words = []
        for text in texts:
            words.extend(re.findall(self.pattern, text))
        
        # Start with character-level vocab
        vocab = {chr(i): i for i in range(256)}
        
        # Build BPE merges
        word_freqs = Counter(words)
        splits = {word: [c for c in word] for word in word_freqs.keys()}
        
        num_merges = self.vocab_size - 256
        for i in range(num_merges):
            pairs = self._get_pairs(splits, word_freqs)
            if not pairs:
                break
            best_pair = max(pairs, key=pairs.get)
            splits = self._merge_pair(best_pair, splits)
            self.merges[best_pair] = len(vocab)
            vocab[''.join(best_pair)] = len(vocab)
        
        self.vocab = vocab
        self.inverse_vocab = {v: k for k, v in vocab.items()}
    
    def _get_pairs(self, splits, word_freqs):
        pairs = Counter()
        for word, freq in word_freqs.items():
            split = splits[word]
            if len(split) < 2:
                continue
            for i in range(len(split) - 1):
                pairs[(split[i], split[i + 1])] += freq
        return pairs
    
    def _merge_pair(self, pair, splits):
        new_splits = {}
        for word, split in splits.items():
            new_split = []
            i = 0
            while i < len(split):
                if i < len(split) - 1 and split[i] == pair[0] and split[i + 1] == pair[1]:
                    new_split.append(pair[0] + pair[1])
                    i += 2
                else:
                    new_split.append(split[i])
                    i += 1
            new_splits[word] = new_split
        return new_splits
    
    def encode(self, text):
        """Encode text to token IDs"""
        tokens = []
        for word in re.findall(self.pattern, text):
            word_tokens = [c for c in word]
            while len(word_tokens) > 1:
                pairs = [(word_tokens[i], word_tokens[i + 1]) for i in range(len(word_tokens) - 1)]
                pair_to_merge = min(pairs, key=lambda p: self.merges.get(p, float('inf')))
                if pair_to_merge not in self.merges:
                    break
                i = 0
                new_tokens = []
                while i < len(word_tokens):
                    if i < len(word_tokens) - 1 and (word_tokens[i], word_tokens[i + 1]) == pair_to_merge:
                        new_tokens.append(word_tokens[i] + word_tokens[i + 1])
                        i += 2
                    else:
                        new_tokens.append(word_tokens[i])
                        i += 1
                word_tokens = new_tokens
            tokens.extend([self.vocab.get(t, 0) for t in word_tokens])
        return tokens
    
    def decode(self, ids):
        """Decode token IDs to text"""
        return ''.join([self.inverse_vocab.get(i, '') for i in ids])
    
    def save(self, path):
        """Save tokenizer"""
        with open(path, 'w') as f:
            json.dump({'vocab': self.vocab, 'merges': {str(k): v for k, v in self.merges.items()}}, f)
    
    def load(self, path):
        """Load tokenizer"""
        with open(path, 'r') as f:
            data = json.load(f)
            self.vocab = data['vocab']
            self.merges = {eval(k): v for k, v in data['merges'].items()}
            self.inverse_vocab = {v: k for k, v in self.vocab.items()}
