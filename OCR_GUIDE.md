# OCR Number Extraction Guide

## Why Numbers Might Be Extracted Incorrectly

The OCR (Optical Character Recognition) system reads numbers from images, but various factors can affect accuracy:

### Common OCR Recognition Issues

| What OCR Sees | What It Reads | Solution |
|--------------|--------------|----------|
| Blurry "0" | "O" (letter) | Take clearer screenshot |
| Poor contrast | Skipped entirely | Improve lighting |
| Small numbers | Partial recognition | Crop to focus area |
| Rotated text | Multiple wrong values | Take straight screenshot |
| Multiple fonts | Inconsistent reading | Use consistent display |

## How to Get Better Extraction

### 1. **Screenshot Quality** ⭐ Most Important
- **High resolution**: 1920x1080 or higher
- **Good lighting**: Avoid glare, shadows, and reflections
- **Clear focus**: Sharp, not blurry text
- **Centered**: Numbers clearly visible in frame

### 2. **Image Composition**
- **Crop tightly**: Focus just on the numbers, remove surrounding UI
- **Maximize size**: Fill the frame with numbers for best OCR
- **Straight angle**: Don't tilt or rotate the screen
- **Minimal text**: Remove instructions, buttons, or other text

### 3. **Best Practices**
```
✅ DO:
- Take screenshot on high-quality display
- Ensure screen is clean
- Use maximum brightness on screen
- Screenshot during clear visibility
- Focus on one display/area at a time

❌ DON'T:
- Use phone camera instead of screenshot
- Take low-resolution screenshots
- Include UI elements around numbers
- Tilt or rotate the image
- Use low screen brightness
```

### 4. **Example Good vs Bad**

#### ❌ Bad Screenshot
- Numbers too small in frame
- Poor contrast
- Surrounding UI included
- Blurry or out of focus

#### ✅ Good Screenshot
- Numbers fill 70-80% of image
- Dark numbers on light background (or vice versa)
- Only numbers visible
- Sharp, in-focus, high-res

## What to Do If Extraction is Wrong

### Option 1: Retake Screenshot
1. Improve image quality (see above)
2. Upload again
3. Check extracted numbers for accuracy

### Option 2: Manual Correction
1. When confirmation modal appears
2. Edit the textarea with correct numbers
3. Manually type/correct numbers if needed
4. Click "Confirm & Run Test"

### Option 3: Use Demo Numbers
1. Skip screenshot upload
2. Manually enter numbers in "Demo Numbers" field
3. Numbers are processed immediately
4. No OCR issues with manual entry

## OCR Extraction Process

Our system tries 5 different strategies to extract numbers:

1. **CLAHE + Otsu Thresholding** - Best for general cases
2. **Image Upscaling** - Enlarges small numbers for better recognition
3. **Adaptive Thresholding** - Good for varying brightness
4. **Binary Threshold + Morphology** - Advanced edge detection
5. **Direct OCR** - Simple approach with Tesseract config

Each strategy tries with error correction:
- O → 0 (letter O becomes number 0)
- l → 1 (letter l becomes number 1)
- S → 5 (letter S becomes number 5)
- B → 8 (letter B becomes number 8)
- And more...

## Testing OCR Quality

### Steps:
1. Take screenshot
2. Upload to our app
3. Review numbers in confirmation modal
4. If numbers are correct → Confirm
5. If numbers are wrong → Edit or retake

## Support for Different Formats

### Screenshots we support:
- Browser screenshots (best)
- Monitor displays
- Roulette display photos (less ideal)
- Digital display screenshots
- Printed and photographed documents

### Screenshots we have trouble with:
- Phone camera photos of screens (use screenshot instead)
- Very small numbers (< 20px height)
- Low resolution images (< 800x600)
- Poor contrast images
- Heavily compressed images

## Advanced Tips

### For Different Displays:

**Computer Screen:**
- Use screenshot tool (Print Screen, Snip, etc.)
- Direct capture = best quality
- No camera needed

**Roulette Display:**
- Take photo with camera
- Ensure proper lighting
- Hold straight to frame
- Use high-quality camera/phone
- Focus on number display only

**Digital Display:**
- Screenshot if possible
- Otherwise, photo with good lighting
- Minimize reflections
- Maximize contrast

## Still Having Issues?

If extraction continues to fail:

1. **Check the image manually** - Open image and verify numbers are readable
2. **Use demo numbers instead** - Enter numbers manually for instant results
3. **Try manual entry** - Type numbers directly, no OCR needed
4. **Report issue** - Include the screenshot for debugging

## Error Messages & Solutions

| Error Message | Cause | Solution |
|--------------|-------|----------|
| "Could not extract numbers" | Poor image quality or no numbers found | Retake screenshot with better quality |
| "No valid numbers found" | Manual entry has non-0-36 numbers | Edit textarea to use only 0-36 |
| "File not selected" | No file uploaded | Click upload area and select image |
| "Invalid file type" | Wrong format uploaded | Use PNG, JPG, JPEG, GIF, or BMP |

## Troubleshooting Steps

1. **First attempt fails?**
   - Check image quality
   - Retake screenshot with better lighting
   - Try uploading again

2. **Numbers partially extracted?**
   - Use confirmation modal to edit
   - Correct numbers before confirming
   - Re-run test if needed

3. **Want to skip OCR?**
   - Use "Demo Numbers" field
   - Enter numbers manually
   - Test runs immediately

## Best Result Settings

| Aspect | Setting |
|--------|---------|
| Screen Brightness | 100% |
| Screen Resolution | 1920x1080+ |
| Image Format | PNG (lossless) |
| Number Size | 30-50px height |
| Contrast | High (dark on light) |
| Screenshot Type | Direct screenshot, not camera |

---

**Remember**: Manual correction is always available in the confirmation modal, so even if OCR isn't perfect, you can fix it before running the strategy test!
