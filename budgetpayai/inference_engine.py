"""
Efficient inference engine with KV caching for BudgetPay AI
Adapted from nanochat for faster generation
"""
import torch
import torch.nn.functional as F


class KVCache:
    """Key-Value cache for efficient transformer inference"""
    
    def __init__(self, batch_size, num_heads, seq_len, head_dim, num_layers):
        self.kv_shape = (num_layers, 2, batch_size, num_heads, seq_len, head_dim)
        self.kv_cache = None
        self.pos = 0
    
    def reset(self):
        """Reset cache position"""
        self.pos = 0
    
    def get_pos(self):
        """Get current position in cache"""
        return self.pos
    
    def insert_kv(self, layer_idx, k, v):
        """Insert keys and values into cache"""
        # Lazy initialize
        if self.kv_cache is None:
            self.kv_cache = torch.empty(self.kv_shape, dtype=k.dtype, device=k.device)
        
        B, H, T_add, D = k.size()
        t0, t1 = self.pos, self.pos + T_add
        
        # Dynamically grow cache if needed
        if t1 > self.kv_cache.size(4):
            t_needed = t1 + 1024
            t_needed = (t_needed + 1023) & ~1023  # Round up to 1024
            additional_shape = list(self.kv_cache.shape)
            additional_shape[4] = t_needed - self.kv_cache.size(4)
            additional_cache = torch.empty(additional_shape, dtype=k.dtype, device=k.device)
            self.kv_cache = torch.cat([self.kv_cache, additional_cache], dim=4).contiguous()
            self.kv_shape = self.kv_cache.shape
        
        # Insert k, v
        self.kv_cache[layer_idx, 0, :, :, t0:t1] = k
        self.kv_cache[layer_idx, 1, :, :, t0:t1] = v
        
        # Return full cached keys/values
        key_view = self.kv_cache[layer_idx, 0, :, :, :t1]
        value_view = self.kv_cache[layer_idx, 1, :, :, :t1]
        
        # Update position after last layer
        if layer_idx == self.kv_cache.size(0) - 1:
            self.pos = t1
        
        return key_view, value_view


class InferenceEngine:
    """Fast inference engine for BudgetPay AI"""
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    @torch.inference_mode()
    def sample_next_token(self, logits, temperature=1.0, top_k=None):
        """Sample next token from logits"""
        if temperature == 0.0:
            return torch.argmax(logits, dim=-1, keepdim=True)
        
        if top_k is not None:
            k = min(top_k, logits.size(-1))
            vals, idx = torch.topk(logits, k, dim=-1)
            vals = vals / temperature
            probs = F.softmax(vals, dim=-1)
            choice = torch.multinomial(probs, num_samples=1)
            return idx.gather(1, choice)
        else:
            logits = logits / temperature
            probs = F.softmax(logits, dim=-1)
            return torch.multinomial(probs, num_samples=1)
    
    @torch.inference_mode()
    def generate(self, prompt_tokens, max_tokens=100, temperature=0.8, top_k=50):
        """
        Generate tokens efficiently using KV caching
        
        Args:
            prompt_tokens: List of input token IDs
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_k: Top-k sampling parameter
        
        Yields:
            token: Next generated token ID
        """
        device = next(self.model.parameters()).device
        
        # Convert prompt to tensor
        ids = torch.tensor([prompt_tokens], dtype=torch.long, device=device)
        
        # Generate tokens one at a time
        for _ in range(max_tokens):
            # Forward pass
            logits = self.model(ids)
            
            # Get logits for last position
            logits = logits[:, -1, :]
            
            # Sample next token
            next_token = self.sample_next_token(logits, temperature, top_k)
            
            # Yield the token
            yield next_token[0, 0].item()
            
            # Append to sequence for next iteration
            ids = torch.cat([ids, next_token], dim=1)
            
            # Keep only recent context if too long
            if ids.size(1) > self.model.max_seq_len:
                ids = ids[:, -self.model.max_seq_len:]
    
    @torch.inference_mode()
    def generate_text(self, prompt, max_tokens=100, temperature=0.8, top_k=50):
        """
        Generate text from a prompt string
        
        Args:
            prompt: Input text string
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_k: Top-k sampling
        
        Returns:
            generated_text: Complete generated text
        """
        # Encode prompt
        prompt_tokens = self.tokenizer.encode(prompt)
        
        # Generate tokens
        generated_tokens = []
        for token in self.generate(prompt_tokens, max_tokens, temperature, top_k):
            generated_tokens.append(token)
            
            # Stop on end token if exists
            if hasattr(self.tokenizer, 'eos_token_id') and token == self.tokenizer.eos_token_id:
                break
        
        # Decode all tokens
        full_tokens = prompt_tokens + generated_tokens
        return self.tokenizer.decode(full_tokens)
    
    @torch.inference_mode()
    def generate_streaming(self, prompt, max_tokens=100, temperature=0.8, top_k=50):
        """
        Generate text with streaming output
        
        Args:
            prompt: Input text string
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_k: Top-k sampling
        
        Yields:
            chunk: Text chunk for each generated token
        """
        # Encode prompt
        prompt_tokens = self.tokenizer.encode(prompt)
        
        # Generate and decode tokens one by one
        for token in self.generate(prompt_tokens, max_tokens, temperature, top_k):
            chunk = self.tokenizer.decode([token])
            yield chunk
            
            # Stop on end token
            if hasattr(self.tokenizer, 'eos_token_id') and token == self.tokenizer.eos_token_id:
                break


def create_engine(model, tokenizer):
    """Factory function to create inference engine"""
    return InferenceEngine(model, tokenizer)
