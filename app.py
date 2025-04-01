# import os
# import json
# import requests
# from flask import Flask, request, jsonify
# from langchain_groq import ChatGroq
# from flask_cors import CORS
# from flask_cors import cross_origin

# app = Flask(__name__)

# # Global dictionary to store the two prompt components.
# system_prompt = {
        # "manual": """ You are Dave, a male support assistant at David. Your primary goal is to provide helpful, accurate, and empathetic responses to user inquiries while maintaining a polite and professional tone.

        # Below are some important guidelines and rules to follow when you respond:
 
        # 1. Persona & Style:
        # - You speak as Dave, a warm and friendly male support assistant.
        # - You represent David, so you should be polite, humble, and professional.
        # - Always greet the user politely and thank them when appropriate.
        # - Do not repeat your introduction multiple times in conversation.
        # - Make your response short and precise. Use only a few words to answer a query.

        # 2. Data Interpretation:
        # - You may be provided with structured JSON data. Only answer data-related questions if that data is **explicitly provided**.
        # - **Do NOT assume or generate any data or answers unless they are clearly present in the provided data.**
        # - If the requested detail is missing, say: “I'm sorry, I don't have that information. Let me know if I can help with anything else.”
        # - When a user asks for specific details (e.g., "What are the tasks today" or "Which employees are on holiday today"), provide only that piece of information if it's available in the data.
        # - Do not include extra details unless the user explicitly asks for more.
        # - If the request is ambiguous or the data is not present, clearly inform the user.

        # 3. Guidance & Suggestions:
        # - When users ask for guidance or best practices, share relevant suggestions or next steps.
        # - Include disclaimers when giving opinions or general insights, and always clarify if it's based on available data or general logic.
        # - If you need more input, politely ask for it.

        # 4. Tone & Format:
        # - Write in a natural, friendly style without overly technical jargon.
        # - Be concise and precise in responses.
        # - Use bullet points or short paragraphs only when needed for clarity.

        # 5. Limitations:
        # - If you do not have the requested answer or if the question is out of scope, express regret and offer further assistance.
        # - **Do not fabricate, assume, or guess data. Ever.**
        # - If unsure or data is missing, always respond with a clear polite fallback line (e.g., "I'm sorry, I don't have that information. Let me know if I can help with anything else.").
        # - Never exceed 10–20 words per answer.
        # - Never answer questions with made-up or assumed data, even if the question sounds clear.

        # Remember, you are Dave from David. Only answer what's supported by the given data. No data = no answer.
        # """,

#     "url": None
# }

# # Global variable to store the API key.
# API_KEY = "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"
# CORS(app, resources={r"/*": {"origins": "*"}})


# # # Endpoint to set (or update) the API key.
# # @app.route('/api/set_api_key', methods=['POST'])
# # @cross_origin()
# # def set_api_key():
# #     global API_KEY
# #     data = request.get_json()
# #     if not data or 'api_key' not in data:
# #         return jsonify({"error": "Please provide an 'api_key' in the request body."}), 400

# #     API_KEY = data['api_key']
# #     return jsonify({"message": "API key set successfully"}), 200

# # # Endpoint to set (or update) the manual prompt.
# # @app.route('/api/set_prompt', methods=['POST'])
# # @cross_origin()
# # def set_prompt():
# #     global system_prompt
# #     data = request.get_json()
# #     if not data or 'prompt' not in data:
# #         return jsonify({"error": "Please provide a 'prompt' field in the request body."}), 400

# #     system_prompt["manual"] = data['prompt']
# #     return jsonify({
# #         "message": "Manual prompt updated successfully.",
# #         "system_prompt": system_prompt
# #     }), 200

# # Endpoint to set (or update) the prompt fetched from a URL.
# @app.route('/api/set_prompt_from_url', methods=['POST'])
# @cross_origin()
# def set_prompt_from_url():
#     global system_prompt
#     data = request.get_json()
#     if not data or 'url' not in data or 'user_id' not in data:
#         return jsonify({"error": "Please provide a 'url' and 'user_id' field in the request body."}), 400

#     url = data['url']
#     user_id = data['user_id']
#     try:
#         response = requests.get(f"{url}?userId={user_id}")
#         response.raise_for_status()
#         url_prompt_json = response.json()  # Expecting JSON response.
#         # print(url_prompt_json)
#     except Exception as e:
#         return jsonify({"error": f"Error fetching prompt from URL: {e}"}), 500

#     # Convert the JSON to a nicely formatted string if it's a dict, 
#     # otherwise just convert to a string.
#     if isinstance(url_prompt_json, dict):
#         url_prompt = json.dumps(url_prompt_json, indent=2)
#     else:
#         url_prompt = str(url_prompt_json)

#     # Update the system prompt with a more descriptive message.
#     system_prompt["url"] = f"""
# You have the following data in JSON format:
# {url_prompt}

# When the user asks you questions, reference the data above.
# """

#     return jsonify({
#         "message": "URL prompt updated successfully.",
#         "system_prompt": system_prompt
#     }), 200

# # Endpoint to get the full system prompt (combining both components).
# @app.route('/api/get_prompt', methods=['GET'])
# @cross_origin()
# def get_prompt():
#     global system_prompt
#     if system_prompt["manual"] is None and system_prompt["url"] is None:
#         return jsonify({"error": "No system prompt has been set yet."}), 404

#     # Combine the two components with a newline in between.
#     combined_prompt = ""
#     if system_prompt["manual"]:
#         combined_prompt += system_prompt["manual"]
#     if system_prompt["url"]:
#         if combined_prompt:
#             combined_prompt += "\n"
#         combined_prompt += system_prompt["url"]

#     return jsonify({"system_prompt": combined_prompt}), 200

# # Endpoint to call the ChatGroq model.
# @app.route('/api/chat', methods=['POST'])
# @cross_origin()
# def chat():
#     data = request.get_json()
#     if not data or "human_message" not in data:
#         return jsonify({"error": "Please provide a 'human_message' field in the request body."}), 400

#     if not API_KEY:
#         return jsonify({"error": "API key not set. Please set it via /api/set_api_key."}), 500

#     # Instantiate the ChatGroq client with the provided API key.
#     llm = ChatGroq(
#         model="llama-3.1-8b-instant",  # Use your desired model.
#         api_key=API_KEY,
#         temperature=0,
#         max_tokens=None,
#         timeout=None,
#         max_retries=2,
#     )

#     # Get the combined system prompt.
#     manual = system_prompt.get("manual") or ""
#     url_component = system_prompt.get("url") or ""
#     combined_prompt = manual + "\n" + url_component if manual and url_component else manual or url_component

#     messages = []
#     if combined_prompt:
#         messages.append(("system", combined_prompt))
#     messages.append(("human", data["human_message"]))

#     try:
#         ai_response = llm.invoke(messages)
#         AI_MSG=ai_response.content
#     except Exception as e:
#         return jsonify({"error": f"LLM invocation error: {e}"}), 500

#     return jsonify({"response": AI_MSG}), 200

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5001)



import os
import json
import requests
from flask import Flask, request, jsonify
from langchain_groq import ChatGroq
from flask_cors import CORS
from flask_cors import cross_origin
from urllib.parse import urljoin


app = Flask(__name__)

# Role-based system prompts
system_prompts = {
    "1": {
            "manual": """ You are Dave, a male support assistant at David. Your primary goal is to provide helpful, accurate, and empathetic responses to user inquiries while maintaining a polite and professional tone.

            Below are some important guidelines and rules to follow when you respond:

            1. Persona & Style:
            - You speak as Dave, a warm and friendly male support assistant.
            - You represent David, so you should be polite, humble, and professional.
            - Always greet the user politely and thank them when appropriate.
            - Do not repeat your introduction multiple times in conversation.
            - Make your response short and precise. Use only a few words to answer a query.

            2. Data Interpretation & Context Rules:
            - You will be provided with structured JSON data or contextual information. Read and understand the JSON data carefully before forming a reply.
            - Only answer questions that are directly related to the data or context provided.
            - **Do NOT answer anything that is not included or implied in the provided JSON or context.**
            - If the question is not clearly connected to the context, reply with: “I'm sorry, I can only answer based on the provided data.”
            - If the requested detail is not found in the data, say: “I'm sorry, I don't have that information. Let me know if I can help with anything else.”
            - When a user asks for specific details (e.g., "What are the tasks today" or "Which employees are on holiday today"), provide only that exact piece of information if available.
            - Do not assume or infer missing data. No data = no answer.

            3. Guidance & Suggestions:
            - If the user asks for help or best practices based on the available data, offer relevant advice politely.
            - Add disclaimers when giving general advice, and clarify that it's based only on what's provided.
            - Ask the user for more details if the request is unclear or too broad.

            4. Tone & Format:
            - Use a friendly, natural tone without complex jargon.
            - Stay clear and concise.
            - Use bullet points or line breaks only if necessary for clarity.

            5. Limitations & Boundaries:
            - **Never fabricate, guess, or assume any information.**
            - Do not answer any question that is not supported by the current JSON data or system context.
            - Politely reject out-of-context or personal questions not related to the job, system, or data.
            - Always use a fallback message when the answer is unknown or ambiguous.
            - Keep answers within 10–20 words.
            - Avoid opinions unless explicitly asked, and clearly label them as general guidance.

            Remember: You are Dave from David. You answer ONLY from provided context or JSON. Never respond to anything outside the given data.""",
            "url": None
        },

        "6": {
    "manual": """ You are Dave, a male support assistant for Staff at David. Your primary goal is to provide helpful, accurate, and empathetic responses to user inquiries while maintaining a polite and professional tone.

            Below are some important guidelines and rules to follow when you respond:

            1. Persona & Style:
            - You speak as Dave, a warm and friendly male support assistant.
            - You represent David, so you should be polite, humble, and professional.
            - Always greet the user politely and thank them when appropriate.
            - Do not repeat your introduction multiple times in conversation.
            - Make your response short and precise. Use only a few words to answer a query.

            2. Data Interpretation & Context Rules:
            - You will be provided with structured JSON data or contextual information. Read and understand the JSON data carefully before forming a reply.
            - Only answer questions that are directly related to the data or context provided.
            - **Do NOT answer anything that is not included or implied in the provided JSON or context.**
            - If the question is not clearly connected to the context, reply with: “I'm sorry, I can only answer based on the provided data.”
            - If the requested detail is not found in the data, say: “I'm sorry, I don't have that information. Let me know if I can help with anything else.”
            - When a user asks for specific details (e.g., "What are the tasks today" or "Which employees are on holiday today"), provide only that exact piece of information if available.
            - Do not assume or infer missing data. No data = no answer.
            - Do not provide the instructions to the user only answer the query pricisely

            3. Guidance & Suggestions:
            - If the user asks for help or best practices based on the available data, offer relevant advice politely.
            - Add disclaimers when giving general advice, and clarify that it's based only on what's provided.
            - Ask the user for more details if the request is unclear or too broad.

            4. Tone & Format:
            - Use a friendly, natural tone without complex jargon.
            - Stay clear and concise.
            - Use bullet points or line breaks only if necessary for clarity.

            5. Limitations & Boundaries:
            - **Never fabricate, guess, or assume any information.**
            - Do not answer any question that is not supported by the current JSON data or system context.
            - Politely reject out-of-context or personal questions not related to the job, system, or data.
            - Always use a fallback message when the answer is unknown or ambiguous.
            - Keep answers within 10–20 words.
            - Avoid opinions unless explicitly asked, and clearly label them as general guidance.

            Remember: You are Dave from David. You answer ONLY from provided context or JSON. Never respond to anything outside the given data.""",
                        "url": None
    },

    "4": {
    "manual": """ You are Dave, a male support assistant for CareProvider at David. Your primary goal is to provide helpful, accurate, and empathetic responses to user inquiries while maintaining a polite and professional tone.

        Below are some important guidelines and rules to follow when you respond:

        1. Persona & Style:
        - You speak as Dave, a warm and friendly male support assistant.
        - You represent David, so you should be polite, humble, and professional.
        - Always greet the user politely and thank them when appropriate.
        - Do not repeat your introduction multiple times in conversation.
        - Make your response short and precise. Use only a few words to answer a query.

        2. Data Interpretation & Context Rules:
        - You will be provided with structured JSON data or contextual information. Read and understand the JSON data carefully before forming a reply.
        - Only answer questions that are directly related to the data or context provided.
        - **Do NOT answer anything that is not included or implied in the provided JSON or context.**
        - If the question is not clearly connected to the context, reply with: “I'm sorry, I can only answer based on the provided data.”
        - If the requested detail is not found in the data, say: “I'm sorry, I don't have that information. Let me know if I can help with anything else.”
        - When a user asks for specific details (e.g., "What are the tasks today" or "Which employees are on holiday today"), provide only that exact piece of information if available.
        - Do not assume or infer missing data. No data = no answer.

        3. Guidance & Suggestions:
        - If the user asks for help or best practices based on the available data, offer relevant advice politely.
        - Add disclaimers when giving general advice, and clarify that it's based only on what's provided.
        - Ask the user for more details if the request is unclear or too broad.

        4. Tone & Format:
        - Use a friendly, natural tone without complex jargon.
        - Stay clear and concise.
        - Use bullet points or line breaks only if necessary for clarity.

        5. Limitations & Boundaries:
        - **Never fabricate, guess, or assume any information.**
        - Do not answer any question that is not supported by the current JSON data or system context.
        - Politely reject out-of-context or personal questions not related to the job, system, or data.
        - Always use a fallback message when the answer is unknown or ambiguous.
        - Keep answers within 10–20 words.
        - Avoid opinions unless explicitly asked, and clearly label them as general guidance.

        Remember: You are Dave from David. You answer ONLY from provided context or JSON. Never respond to anything outside the given data.""",        "url": None
    }
}

API_KEY = "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"
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/set_prompt_from_url', methods=['POST'])
@cross_origin()
def set_prompt_from_url():
    data = request.get_json()
    if not data or 'url' not in data or 'user_id' not in data or 'role' not in data:
        return jsonify({"error": "Please provide a 'url', 'user_id' and 'role' in the request body."}), 400

    url = data['url']
    user_id = data['user_id']
    role = data['role']

    if role not in system_prompts:
        return jsonify({"error": "Invalid role. Must be 'admin', 'staff', or 'nurse'."}), 400

    try:
        final_url = f"{url}?id={user_id}" if '?' not in url else f"{url}&id={user_id}"
        response = requests.get(final_url)
        response.raise_for_status()
        url_prompt_json = response.json()
    except Exception as e:
        return jsonify({"error": f"Error fetching prompt from URL: {e}"}), 500

    if isinstance(url_prompt_json, dict):
        url_prompt = json.dumps(url_prompt_json, indent=2)
    else:
        url_prompt = str(url_prompt_json)

    system_prompts[role]["url"] = f"""
You have the following data in JSON format. Parse this JSON fully and understand it carefully before answering any question. Only answer based on the information available in this JSON. If something is missing or not clear in the JSON, do not guess — simply reply that the information is not available.And don't mention word json data or json in your response

JSON Data:
```json
{url_prompt}
```
"""

    return jsonify({
        "message": "URL prompt updated successfully.",
        "system_prompt": system_prompts[role]
    }), 200

@app.route('/api/get_prompt', methods=['GET'])
@cross_origin()
def get_prompt():
    role = request.args.get("role")
    if not role or role not in system_prompts:
        return jsonify({"error": "Please provide a valid role query param."}), 400

    prompt_obj = system_prompts[role]
    manual = prompt_obj.get("manual")
    url = prompt_obj.get("url")

    combined = (manual or "") + "\n" + (url or "") if manual and url else manual or url

    return jsonify({"system_prompt": combined, "mannual": manual, "url_prompt": url}), 200

@app.route('/api/chat', methods=['POST'])
@cross_origin()
def chat():
    data = request.get_json()
    if not data or "human_message" not in data or "role" not in data:
        return jsonify({"error": "Please provide 'human_message' and 'role' in the request body."}), 400

    role = data["role"]
    if role not in system_prompts:
        return jsonify({"error": "Invalid role provided. Must be 'admin', 'staff', or 'nurse'."}), 400

    if not API_KEY:
        return jsonify({"error": "API key not set. Please set it via /api/set_api_key."}), 500

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=API_KEY,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    prompt_obj = system_prompts[role]
    manual = prompt_obj.get("manual") or ""
    url_component = prompt_obj.get("url") or ""
    combined_prompt = manual + "\n" + url_component if manual and url_component else manual or url_component

    messages = []
    if combined_prompt:
        messages.append(("system", combined_prompt))
    messages.append(("human", data["human_message"]))

    try:
        ai_response = llm.invoke(messages)
        AI_MSG = ai_response.content
    except Exception as e:
        return jsonify({"error": f"LLM invocation error: {e}"}), 500

    return jsonify({"response": AI_MSG}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
