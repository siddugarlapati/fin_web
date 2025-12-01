"""
Training loop for Aiza with advanced features
"""
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.nn.parallel import DistributedDataParallel as DDP
from tqdm import tqdm
import os


class AizaTrainer:
    def __init__(self, model, train_data, val_data=None, lr=3e-4, device='cuda', 
                 weight_decay=0.1, grad_clip=1.0, warmup_steps=100):
        self.model = model.to(device)
        self.train_data = train_data
        self.val_data = val_data
        self.device = device
        self.grad_clip = grad_clip
        self.warmup_steps = warmup_steps
        self.step = 0
        
        # Advanced optimizer with weight decay
        self.optimizer = torch.optim.AdamW(
            model.parameters(), 
            lr=lr, 
            weight_decay=weight_decay,
            betas=(0.9, 0.95)
        )
        
        # Learning rate scheduler
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, 
            T_max=10000
        )
        
    def train_epoch(self, dataloader):
        self.model.train()
        total_loss = 0
        
        for batch in tqdm(dataloader, desc="Training"):
            x, y = batch
            x, y = x.to(self.device), y.to(self.device)
            
            # Forward pass
            logits = self.model(x)
            loss = nn.functional.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
            
            # Backward pass
            self.optimizer.zero_grad()
            loss.backward()
            
            # Gradient clipping
            if self.grad_clip > 0:
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_clip)
            
            self.optimizer.step()
            
            # Learning rate warmup
            if self.step < self.warmup_steps:
                lr_scale = min(1.0, (self.step + 1) / self.warmup_steps)
                for param_group in self.optimizer.param_groups:
                    param_group['lr'] = lr_scale * 3e-4
            else:
                self.scheduler.step()
            
            self.step += 1
            total_loss += loss.item()
        
        return total_loss / len(dataloader)
    
    @torch.no_grad()
    def validate(self, dataloader):
        self.model.eval()
        total_loss = 0
        
        for batch in dataloader:
            x, y = batch
            x, y = x.to(self.device), y.to(self.device)
            
            logits = self.model(x)
            loss = nn.functional.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
            total_loss += loss.item()
        
        return total_loss / len(dataloader)
    
    def train(self, num_epochs, batch_size=32, save_every=1):
        train_loader = DataLoader(self.train_data, batch_size=batch_size, shuffle=True)
        best_val_loss = float('inf')
        
        for epoch in range(num_epochs):
            train_loss = self.train_epoch(train_loader)
            current_lr = self.optimizer.param_groups[0]['lr']
            print(f"Epoch {epoch + 1}/{num_epochs} - Train Loss: {train_loss:.4f} - LR: {current_lr:.6f}")
            
            if self.val_data:
                val_loader = DataLoader(self.val_data, batch_size=batch_size)
                val_loss = self.validate(val_loader)
                print(f"Validation Loss: {val_loss:.4f}")
                
                # Save best model
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    self.save_checkpoint('aiza_best.pt')
                    print(f"✓ Saved best model (val_loss: {val_loss:.4f})")
            
            # Regular checkpoint
            if (epoch + 1) % save_every == 0:
                self.save_checkpoint(f'aiza_epoch_{epoch+1}.pt')
    
    def save_checkpoint(self, path):
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, path)
    
    def load_checkpoint(self, path):
        checkpoint = torch.load(path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
