# diffusion

##On Mac
```
export MODEL_NAME="stabilityai/stable-diffusion-xl-base-1.0"
export DATASET_NAME="./3d_icon"
export OUTPUT_DIR="3d-icon-SDXL-LoRA"
export VAE_PATH="madebyollin/sdxl-vae-fp16-fix"

accelerate launch train_dreambooth_lora_sdxl_advanced.py \
--pretrained_model_name_or_path=$MODEL_NAME \
--pretrained_vae_model_name_or_path=$VAE_PATH \
--dataset_name=$DATASET_NAME \
--instance_prompt="3d icon in the style of TOK" \
--validation_prompt="a TOK icon of an astronaut riding a horse, in the style of TOK" \
--output_dir=$OUTPUT_DIR \
--caption_column="prompt" \
--mixed_precision="bf16" \
--resolution=1024 \
--train_batch_size=3 \
--repeats=1 \
--report_to="wandb"\
--gradient_accumulation_steps=1 \
--gradient_checkpointing \
--learning_rate=1.0 \
--text_encoder_lr=1.0 \
--optimizer="prodigy"\
--train_text_encoder_ti\
--train_text_encoder_ti_frac=0.5\
--snr_gamma=5.0 \
--lr_scheduler="constant" \
--lr_warmup_steps=0 \
--rank=8 \
--max_train_steps=1000 \
--checkpointing_steps=2000 \
--seed="0"
```

##On PC

```
#!/bin/bash

# Set environment variables
export MODEL_NAME="stabilityai/stable-diffusion-xl-base-1.0"
export DATASET_NAME="./3d_icon"
export OUTPUT_DIR="3d-icon-SDXL-LoRA"
export VAE_PATH="madebyollin/sdxl-vae-fp16-fix"

# Run the accelerate command
accelerate launch train_dreambooth_lora_sdxl_advanced.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --pretrained_vae_model_name_or_path=$VAE_PATH \
  --dataset_name=$DATASET_NAME \
  --instance_prompt="3d icon in the style of TOK" \
  --validation_prompt="a TOK icon of an astronaut riding a horse, in the style of TOK" \
  --output_dir=$OUTPUT_DIR \
  --caption_column="prompt" \
  --mixed_precision="no" \
  --resolution=1024 \
  --train_batch_size=3 \
  --repeats=1 \
  --report_to="wandb" \
  --gradient_accumulation_steps=1 \
  --gradient_checkpointing \
  --learning_rate=1.0 \
  --text_encoder_lr=1.0 \
  --optimizer="prodigy" \
  --train_text_encoder_ti \
  --train_text_encoder_ti_frac=0.5 \
  --snr_gamma=5.0 \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --rank=8 \
  --max_train_steps=1000 \
  --checkpointing_steps=2000 \
  --seed="0"

```
