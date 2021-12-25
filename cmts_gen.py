"""
Instagram comments generation using OpenAI API Completion fucntion
"""

import os
import openai

openai.organization = "org-BcujbtBxj3ZIAfRsoyxnNVRy"
openai.api_key = os.getenv("OPENAI_API_KEY") # SECRET!! DO NOT SHOW in public
openai.Engine.list()

