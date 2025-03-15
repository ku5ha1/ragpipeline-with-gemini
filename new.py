import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyAxjyL24yv50VR5P-IWEn7wDfoP0GuhxAU")

# List available models
models = genai.list_models()
for model in models:
    print(model.name)