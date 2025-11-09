# Image, Video, and Audio Embeddings Guide

---

## Quick Overview

Embeddings aren't just for text! We can create embeddings for images, videos, and audio too. These embeddings help us find similar items.

**Main Idea**: Convert media files → numerical vectors → compare similarity

---

## Part 1: Image Embeddings

### What are Image Embeddings?

A single number vector (list of numbers) that represents what an image looks like. Two similar images will have similar vectors.

### The Model: ResNet-18

**What is it?**: A pre-trained deep learning model trained on millions of images to recognize objects.

**Key Idea**: 
- ResNet-18 is designed for image classification
- But we don't want classification (what object is this?)
- We want embeddings (what features does this image have?)

**Solution**: Remove the final classification layer and extract features from the last hidden layer

### How It Works

```
Image (224×224 pixels) 
    ↓
ResNet-18 (18 layers)
    ↓
Remove last classification layer
    ↓
Extract features (2048-dimensional vector)
    ↓
Image Embedding
```

### Process - Step by Step

**Step 1: Load Pretrained Model**
- Use ResNet-18 trained on ImageNet (large image dataset)
- Model already understands visual patterns from pretraining

**Step 2: Preprocess Image**
- Resize to 224×224 pixels (what ResNet expects)
- Convert to tensor format
- Normalize pixel values

```python
# Brief example
image = PIL.Image.open("pen.jpg")
image = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224)
])(image)
```

**Step 3: Extract Features**
- Pass image through all 18 layers
- Get output from second-to-last layer (before classification)
- Flatten into 1D vector

```python
embedding = model(image)  # Skip final layer
embedding = embedding.flatten()  # Make 1D
```

**Step 4: Use for Similarity**
- Compare embeddings using cosine similarity
- Similar images = high similarity score (close to 1)
- Different images = low similarity score (close to 0)

### Case Study: Pen Image Search

**Scenario**: Find all pen images in a folder

**Process**:
1. Generate embedding for query pen image
2. Generate embeddings for all images in folder
3. Calculate similarity scores
4. Rank by similarity
5. Show top matching pens

**Result**: Pen images matched with other pen images, cups with cups, etc.

---

## Part 2: Video Embeddings

### What are Video Embeddings?

A vector representing the entire video's content - both spatial (what you see) and temporal (how it changes over time).

### The Model: R3D-18 (3D CNN)

**What's Different?**: Regular CNNs only look at single images. 3D CNNs look at sequences of frames.

**Why 3D?**:
- Height × Width = space (what's in the frame)
- Time = sequence of frames
- 3D CNN captures spatial AND temporal features

### How It Works

```
Video Frames [Frame1, Frame2, Frame3, ...]
    ↓
R3D-18 (3D Convolutional Layers)
    ↓
Learns spatial patterns within frames
Learns temporal patterns between frames
    ↓
Video Embedding
```

### Process - Step by Step

**Step 1: Load Pretrained 3D CNN**
- R3D-18 pretrained on video action recognition
- Understands motion and scenes

**Step 2: Extract Video Frames**
- Read video file frame by frame
- Convert to RGB format
- Resize to 224×224

```python
video = cv2.VideoCapture("park.mp4")
frames = []
while video.isOpened():
    ret, frame = video.read()
    frames.append(frame)
```

**Step 3: Process Frames**
- Stack frames together
- Normalize pixel values
- Pass through 3D CNN

**Step 4: Get Embedding**
- Output from 3D CNN is video embedding
- Single vector represents entire video

### Case Study: Video Similarity

**Scenario**: Find similar videos of kids playing

**Process**:
1. Query: Video of kids playing in park
2. Generate embedding for query video
3. Generate embeddings for all videos
4. Calculate similarity
5. Return top similar videos

**Result**: Videos of kids → matched with other kid videos, water videos → matched with water videos

**Note**: Processing videos is slow (takes time to extract all frames)

---

## Part 3: Audio Embeddings

### What are Audio Embeddings?

A vector representing what an audio sounds like - capturing pitch, timbre, and other acoustic features.

### The Model: Mel Spectrogram

**What is it?**: NOT a neural network. It's a feature extraction technique.

**Why Mel Spectrogram?**:
- Converts audio waveforms to frequency representation
- "Mel" scale mimics human ear perception
- Better than raw audio for ML models

### How It Works

```
Audio Waveform (sound wave data)
    ↓
Fourier Transform (convert to frequencies)
    ↓
Apply Mel Scale (human-like frequency perception)
    ↓
Convert to Spectrogram (visual representation)
    ↓
Collapse to 1D (audio embedding)
    ↓
Audio Embedding
```

### Process - Step by Step

**Step 1: Load Audio**
- Read audio file
- Resample to standard rate (e.g., 16,000 samples/second)
- Convert to mono (single channel)

```python
waveform, sample_rate = torchaudio.load("voice.mp3")
waveform = torchaudio.transforms.Resample(
    sample_rate, 16000)(waveform)
```

**Step 2: Compute Mel Spectrogram**
- Convert audio to frequency domain
- Apply mel scale
- Get 2D spectrogram (frequency × time)

**Step 3: Normalize**
- Normalize spectrogram values
- Makes features comparable

**Step 4: Collapse to 1D**
- Average across time dimension
- Single vector = audio embedding

### Case Study: Voice Gender Detection

**Scenario**: Find female voices among mix of male and female voices

**Process**:
1. Query: Female voice saying "Life is beautiful"
2. Generate embedding for query
3. Generate embeddings for all audio files
4. Calculate similarity
5. Return top matches

**Result**: Female voice matched with other female voices, male with male

---

## Comparing All Three

| Type | Model | Input | Captures | Use Case |
|------|-------|-------|----------|----------|
| Image | ResNet-18 | Image | Visual features | Find similar images |
| Video | R3D-18 | Video frames | Spatial + temporal | Find similar videos |
| Audio | Mel Spectrogram | Audio waveform | Frequency + pitch | Find similar sounds |

---

## Common Pattern: Semantic Search

All three follow the same pattern:

```
Step 1: Generate Embedding for Query
Step 2: Generate Embeddings for All Items
Step 3: Calculate Similarity (Cosine)
Step 4: Rank by Similarity
Step 5: Return Top N Results
```

### Why Cosine Similarity?

It measures angle between vectors (0 to 1 score):
- 1.0 = identical
- 0.5 = moderately similar
- 0.0 = completely different

---

## Key Concepts

**Pretraining**: Models are trained on large datasets first, then reused for embeddings

**Feature Extraction**: Remove final layer to get internal representations instead of classifications

**Preprocessing**: Convert raw media to format the model expects

**Embedding Dimension**:
- Image: 2,048 dimensions (ResNet-18)
- Video: Depends on model
- Audio: Depends on spectrogram resolution

**Similarity Comparison**: Embeddings allow fast comparison (just math on vectors)

---

## Real-World Applications

**Image**: E-commerce product search, duplicate detection, visual search

**Video**: Video recommendation, action recognition, content moderation

**Audio**: Music recommendation, speaker identification, voice-based search

---

## Important Note on Performance

**For production use**: Store embeddings in a vector database

**Why?**:
- Computing embeddings for every query is slow
- Generate embeddings ONCE, store them
- Query becomes simple: just compare vectors
- Vector databases index embeddings for fast retrieval

---

## Summary

- **Image embeddings** capture what's IN the image
- **Video embeddings** capture what happens ACROSS frames
- **Audio embeddings** capture acoustic properties
- All use **semantic search** to find similar items
- All follow same pattern: extract → compare → rank