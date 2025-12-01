"""
Advanced checkpoint management for BudgetPay AI
Adapted from nanochat for better model saving/loading
"""
import os
import glob
import json
import torch


class CheckpointManager:
    """Manage model checkpoints with metadata"""
    
    def __init__(self, checkpoint_dir="checkpoints"):
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(checkpoint_dir, exist_ok=True)
    
    def save_checkpoint(self, step, model, optimizer=None, meta_data=None):
        """Save model, optimizer, and metadata"""
        # Save model
        model_path = os.path.join(self.checkpoint_dir, f"model_{step:06d}.pt")
        torch.save({
            'model_state_dict': model.state_dict(),
            'step': step
        }, model_path)
        print(f"✓ Saved model to: {model_path}")
        
        # Save optimizer if provided
        if optimizer is not None:
            optim_path = os.path.join(self.checkpoint_dir, f"optim_{step:06d}.pt")
            torch.save({
                'optimizer_state_dict': optimizer.state_dict(),
                'step': step
            }, optim_path)
            print(f"✓ Saved optimizer to: {optim_path}")
        
        # Save metadata
        if meta_data is not None:
            meta_path = os.path.join(self.checkpoint_dir, f"meta_{step:06d}.json")
            with open(meta_path, 'w') as f:
                json.dump(meta_data, f, indent=2)
            print(f"✓ Saved metadata to: {meta_path}")
    
    def load_checkpoint(self, step=None, device='cpu', load_optimizer=False):
        """Load model, optimizer, and metadata"""
        if step is None:
            step = self.find_last_step()
        
        # Load model
        model_path = os.path.join(self.checkpoint_dir, f"model_{step:06d}.pt")
        checkpoint = torch.load(model_path, map_location=device)
        model_state = checkpoint['model_state_dict']
        
        # Load optimizer if requested
        optimizer_state = None
        if load_optimizer:
            optim_path = os.path.join(self.checkpoint_dir, f"optim_{step:06d}.pt")
            if os.path.exists(optim_path):
                optim_checkpoint = torch.load(optim_path, map_location=device)
                optimizer_state = optim_checkpoint['optimizer_state_dict']
        
        # Load metadata
        meta_data = None
        meta_path = os.path.join(self.checkpoint_dir, f"meta_{step:06d}.json")
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                meta_data = json.load(f)
        
        return model_state, optimizer_state, meta_data
    
    def find_last_step(self):
        """Find the latest checkpoint step"""
        checkpoint_files = glob.glob(os.path.join(self.checkpoint_dir, "model_*.pt"))
        if not checkpoint_files:
            raise FileNotFoundError(f"No checkpoints found in {self.checkpoint_dir}")
        
        steps = [int(os.path.basename(f).split("_")[1].split(".")[0]) for f in checkpoint_files]
        return max(steps)
    
    def list_checkpoints(self):
        """List all available checkpoints"""
        checkpoint_files = glob.glob(os.path.join(self.checkpoint_dir, "model_*.pt"))
        steps = sorted([int(os.path.basename(f).split("_")[1].split(".")[0]) for f in checkpoint_files])
        return steps
    
    def delete_old_checkpoints(self, keep_last=3):
        """Delete old checkpoints, keeping only the last N"""
        steps = self.list_checkpoints()
        if len(steps) <= keep_last:
            return
        
        steps_to_delete = steps[:-keep_last]
        for step in steps_to_delete:
            # Delete model
            model_path = os.path.join(self.checkpoint_dir, f"model_{step:06d}.pt")
            if os.path.exists(model_path):
                os.remove(model_path)
            
            # Delete optimizer
            optim_path = os.path.join(self.checkpoint_dir, f"optim_{step:06d}.pt")
            if os.path.exists(optim_path):
                os.remove(optim_path)
            
            # Delete metadata
            meta_path = os.path.join(self.checkpoint_dir, f"meta_{step:06d}.json")
            if os.path.exists(meta_path):
                os.remove(meta_path)
        
        print(f"✓ Deleted {len(steps_to_delete)} old checkpoints")
