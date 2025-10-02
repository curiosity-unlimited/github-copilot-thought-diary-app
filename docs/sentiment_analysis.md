# Sentiment Analysis

The Thought Diary application includes AI-powered sentiment analysis to help users identify positive and negative thinking patterns in their diary entries.

## Overview

The sentiment analysis feature uses the GitHub Models inference API to analyze text content and highlight:
- Positive emotions, thoughts, and words with a green background
- Negative emotions, thoughts, and words with a red background

## Architecture

The sentiment analysis functionality is built with the following components:

1. **GitHub Models Service**: Core service that communicates with the GitHub Models API.
2. **Sentiment Analyzer**: Facade that provides a simple interface for the application.
3. **ThoughtDiary Integration**: Method to analyze and store sentiment-analyzed content.

## Configuration

To use the sentiment analysis feature, you need to:

1. Create a GitHub Personal Access Token with the `models: read` permission:
   - Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
   - Create a new token with the `models: read` permission
   - Copy the token value

2. Set the following environment variables in your `.env` file:
   ```
   # Required
   GITHUB_API_KEY=your_token_here
   
   # Optional - defaults shown below
   GITHUB_MODEL=openai/gpt-4o     # Model ID in {publisher}/{model_name} format
   GITHUB_MAX_TOKENS=1000         # Maximum tokens for response generation
   ```

3. Ensure these environment variables are kept secure and not committed to version control

## Usage

### Analyzing Content

The ThoughtDiary model has an `analyze_content()` method to analyze diary entries:

```python
# Create a thought diary entry
diary = ThoughtDiary(
    user_id=current_user.id,
    content="I felt both excitement and anxious after I got elected."
)
db.session.add(diary)
db.session.commit()

# Analyze the content
success, error = diary.analyze_content()
if success:
    db.session.commit()  # Save the analyzed content
else:
    print(f"Analysis failed: {error}")
```

### Displaying Analyzed Content

The analyzed content includes HTML span elements for highlighting:

```html
I felt both <span class="positive">excitement</span> and <span class="negative">anxious</span> after I got elected.
```

Apply CSS styles to render the highlights:

```css
span.positive {
    background-color: green;
    color: white;
}
span.negative {
    background-color: red;
    color: white;
}
```

## GitHub Models API

The service uses the `/inference/chat/completions` endpoint with:
- Authentication via Bearer token
- JSON payload with model ID and message content
- Non-streaming response format

## Technical Details

- **Model**: Configurable via `GITHUB_MODEL` environment variable (default: OpenAI GPT-4o)
- **Max Tokens**: Configurable via `GITHUB_MAX_TOKENS` environment variable (default: 1000)
- **Temperature**: 0.3 (fixed for more consistent results)
- **Supported Models**: Any model available on the GitHub Models platform

## Error Handling

The sentiment analysis service handles various error conditions:
- Missing API key
- API request failures
- Unexpected response formats
- Empty text content