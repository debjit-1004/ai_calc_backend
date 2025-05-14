﻿# import torch
# from transformers import pipeline, BitsAndBytesConfig, AutoProcessor, LlavaForConditionalGeneration
# from PIL import Image

# # quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
# quantization_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_compute_dtype=torch.float16
# )


# model_id = "llava-hf/llava-1.5-7b-hf"
# processor = AutoProcessor.from_pretrained(model_id)
# model = LlavaForConditionalGeneration.from_pretrained(model_id, quantization_config=quantization_config, device_map="auto")
# # pipe = pipeline("image-to-text", model=model_id, model_kwargs={"quantization_config": quantization_config})

# def analyze_image(image: Image):
#     prompt = "USER: <image>\nAnalyze the equation or expression in this image, and return answer in format: {expr: given equation in LaTeX format, result: calculated answer}"

#     inputs = processor(prompt, images=[image], padding=True, return_tensors="pt").to("cuda")
#     for k, v in inputs.items():
#         print(k,v.shape)

#     output = model.generate(**inputs, max_new_tokens=20)
#     generated_text = processor.batch_decode(output, skip_special_tokens=True)
#     for text in generated_text:
#         print(text.split("ASSISTANT:")[-1])





import google.generativeai as genai
import ast
import json
import re
from PIL import Image
from constants import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def analyze_image(img: Image, dict_of_vars: dict):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    dict_of_vars_str = json.dumps(dict_of_vars, ensure_ascii=False)
    prompt = (
        "You have been given an image with some mathematical expressions, equations, or graphical problems, and you need to solve them. "
        "Note: Use the PEMDAS rule for solving mathematical expressions. PEMDAS stands for the Priority Order: Parentheses, Exponents, Multiplication and Division (from left to right), Addition and Subtraction (from left to right). Parentheses have the highest priority, followed by Exponents, then Multiplication and Division, and lastly Addition and Subtraction. "
        "For example: "
        "Q. 2 + 3 * 4 "
        "(3 * 4) => 12, 2 + 12 = 14. "
        "Q. 2 + 3 + 5 * 4 - 8 / 2 "
        "5 * 4 => 20, 8 / 2 => 4, 2 + 3 => 5, 5 + 20 => 25, 25 - 4 => 21. "
        "YOU CAN HAVE FIVE TYPES OF EQUATIONS/EXPRESSIONS IN THIS IMAGE, AND ONLY ONE CASE SHALL APPLY EVERY TIME: "
        "Following are the cases: "
        "1. Simple mathematical expressions like 2 + 2, 3 * 4, 5 / 6, 7 - 8, etc.: In this case, solve and return the answer in the format of a LIST OF ONE DICT [{'expr': given expression, 'result': calculated answer}]. "
        "2. Set of Equations like x^2 + 2x + 1 = 0, 3y + 4x = 0, 5x^2 + 6y + 7 = 12, etc.: In this case, solve for the given variable, and the format should be a COMMA SEPARATED LIST OF DICTS, with dict 1 as {'expr': 'x', 'result': 2, 'assign': True} and dict 2 as {'expr': 'y', 'result': 5, 'assign': True}. This example assumes x was calculated as 2, and y as 5. Include as many dicts as there are variables. "
        "3. Assigning values to variables like x = 4, y = 5, z = 6, etc.: In this case, assign values to variables and return another key in the dict called {'assign': True}, keeping the variable as 'expr' and the value as 'result' in the original dictionary. RETURN AS A LIST OF DICTS. "
        "4. Analyzing Graphical Math problems, which are word problems represented in drawing form, such as cars colliding, trigonometric problems, problems on the Pythagorean theorem, adding runs from a cricket wagon wheel, etc. These will have a drawing representing some scenario and accompanying information with the image. PAY CLOSE ATTENTION TO DIFFERENT COLORS FOR THESE PROBLEMS. You need to return the answer in the format of a LIST OF ONE DICT [{'expr': given expression, 'result': calculated answer}]. "
        "5. Detecting Abstract Concepts that a drawing might show, such as love, hate, jealousy, patriotism, or a historic reference to war, invention, discovery, quote, etc. USE THE SAME FORMAT AS OTHERS TO RETURN THE ANSWER, where 'expr' will be the explanation of the drawing, and 'result' will be the abstract concept. "
        "Analyze the equation or expression in this image and return the answer according to the given rules: "
        "Make sure to use extra backslashes for escape characters like \\f -> \\\\f, \\n -> \\\\n, etc. "
        f"Here is a dictionary of user-assigned variables. If the given expression has any of these variables, use its actual value from this dictionary accordingly: {dict_of_vars_str}. "
        "DO NOT USE BACKTICKS OR MARKDOWN FORMATTING. "
        "PROPERLY QUOTE THE KEYS AND VALUES IN THE DICTIONARY FOR EASIER PARSING WITH Python's ast.literal_eval."
    )
    response = model.generate_content([prompt, img])
    response_text = response.text
    print(response_text)
    # answers = []
    # raw_text = response.text.strip()
    # # Try ast.literal_eval first
    # try:
    #     answers = ast.literal_eval(raw_text)
    # except Exception as e1:
    #     print(f"ast.literal_eval failed: {e1}")
    #     # Try to fix to valid JSON and load
    #     try:
    #         fixed_text = raw_text
    #         # Replace single quotes with double quotes for keys and values
    #         fixed_text = re.sub(r"'", '"', fixed_text)
    #         # Replace True/False with true/false for JSON
    #         fixed_text = fixed_text.replace("True", "true").replace("False", "false")
    #         answers = json.loads(fixed_text)
    #     except Exception as e2:
    #         print(f"json.loads failed: {e2}")
    #         # Last resort: regex extraction
    #         pattern = r"\{'expr':\s*'([^']*)',\s*'result':\s*'([^']*)'(?:,\s*'assign':\s*(True|False))?\}"
    #         matches = re.findall(pattern, raw_text)
    #         if matches:
    #             for expr, result, assign in matches:
    #                 answers.append({
    #                     "expr": expr,
    #                     "result": result,
    #                     "assign": assign == "True" if assign else False
    #                 })
    # print('returned answer', answers)
    # # Ensure assign key
    # for answer in answers:
    #     if 'assign' not in answer:
    #         answer['assign'] = False
    # return answers
    print(response_text[0]['result'])
    return response_text[0]['result']
